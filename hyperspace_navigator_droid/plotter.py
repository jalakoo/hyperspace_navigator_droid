from database import get_plot_path, system_exists
from secrets_util import OPENAI_KEY
from openai import OpenAI
import json

CLIENT = OpenAI(
    api_key=OPENAI_KEY,
)

def extract_locations(sentence)->str:

    prompt = f'You are a navigation droid from the Star Wars universe. Extract the from and to star systems from a sentence and return a json object with the keys "from" and "to", like {{"from":"Alderaan", "to":"Coruscant"}}.'

    response = CLIENT.chat.completions.create(
    model="gpt-3.5-turbo-1106", 
    response_format = {"type":"json_object"},
    messages=[
        {
            "role":"system",
            "content": prompt
        },
        {
            "role":"user",
            "content": sentence
        }
    ],
    max_tokens=60,
    n=1,
    stop=None,
    temperature=0.5,
    )

    extracted = response.choices[0].message.content

    print(f'Locations extracted from question: {extracted}')

    return extracted

class InvalidStartLocation(Exception):
    pass
class InvalidEndLocation(Exception):
    pass

def get_plot(sentence):
    """Get a list of systems and system data for a shortest course plot from one start system to another.

    Args:
        sentence (str): Natural language question asking for directions

    Returns:
        list: List of dictionaries containing system data for course, starting with origin/start system and ending with destination/end system.
    """
    locations = extract_locations(sentence)

    # Verify locations are valid systems
    print(f'Locations type: {type(locations)}')
    locations_dict = json.loads(locations)
    from_ = locations_dict['from']
    to_ = locations_dict['to']
    from_exists = system_exists(from_)
    to_exists = system_exists(to_)
    if from_exists is False:
        raise InvalidStartLocation(from_)  
    if to_exists is False:
        raise InvalidEndLocation(to_)

    # TODO: Fuzzy search match locations if not exact match

    plot = get_plot_path(from_, to_)

    return plot
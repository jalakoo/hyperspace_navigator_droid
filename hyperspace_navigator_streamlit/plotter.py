import requests
from models import System
from secrets import PLOTTER_URL

def post(url, payload) -> list[System]:
    headers = {
        'Content-Type': 'application/json'
        }

    # if BASIC_AUTH is not None:
    #     headers["Authorization"] = BASIC_AUTH

    try:
        response = requests.post(url, data=payload, headers=headers)

        content = response.json()
        result = []
        for s in content:
            try:
                system = System(**s)
                result.append(system)
            except Exception as e:
                print(f'Problem system from course plot: {e}, for system: {s}')
        return result
    
    except Exception as e:
        print(f'Problem getting course plot: {e} from url: {url}, payload: {payload}')
        return None

from openai import OpenAI

CLIENT = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def extract_locations(sentence):

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

def get_plot(sentence):
    """Get a list of systems and system data for a shortest course plot from one start system to another.

    Args:
        sentence (str): Natural language question asking for directions

    Returns:
        list: List of dictionaries containing system data for course, starting with origin/start system and ending with destination/end system.
    """
    locations = extract_locations(sentence)
    
    # TODO: Validate format and locations are available
    # TODO: Fuzzy search match locations if not exact match

    plot = post(PLOTTER_URL, locations)

    return plot
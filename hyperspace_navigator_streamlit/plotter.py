import requests
from models import System
from neo4j import GraphDatabase, basic_auth
from secrets_util import PLOTTER_URL, OPENAI_KEY, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE
from openai import OpenAI
import streamlit as st
import json
@st.cache_data
def system_exists(system: str):
    query = """
    MATCH (n:System)
    WHERE n.name = $systemName
    RETURN n.name as name, n.X as x, n.Y as y, n.Region as region, n.type as type, n.importance as importance
    """
    with GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)) as driver:
        params = {
            "systemName": system
        }
        records, _, _ = driver.execute_query(query,params, database=NEO4J_DATABASE)
        result = []
        for r in records:
            try:
                s = System(**r)
                result.append(s)
            except Exception as e:
                print(f'Error parsing system record: {r}. Error: {e}')
                continue
        print(f'{len(result)} matching systems found')
        return len(result) > 0


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


CLIENT = OpenAI(
    # This is the default and can be omitted
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

    plot = post(PLOTTER_URL, locations)

    return plot
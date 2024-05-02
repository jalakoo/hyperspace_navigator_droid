from openai import OpenAI
from plotter import get_plot, InvalidEndLocation, InvalidStartLocation
from secrets_util import OPENAI_KEY
from database import get_system_info

CLIENT = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_KEY,
)

SYS_PROMPT = f'You are an friendly astro droid from the Star Wars universe. Fulfill navigation queries and general star system related questions for your master pilot. Respond in the style of the character R2-D2, but in English'

MESSAGES = [
        {
            "role":"system",
            "content": SYS_PROMPT
        },
        {
            "role":"user",
            "content": "Please introduce yourself in 1-2 sentences, and end by asking me a question."
        }
    ]

DEFAULT_GREETING = "Greetings, master pilot! I am your friendly astro droid, here to assist with all your navigation and star system queries. How may I assist you with your galactic travels today?"

def welcome_message():

    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=MESSAGES,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.8,
    )

    print(f'welcome response: {response}')

    return response.choices[0].message.content

def plotted_answer(plot, question)-> str:

    converted_plot = str([s.dict() for s in plot])

    PROMPT = f'Answer questions regarding a hyperspace jump course from a list of dictionary objects. Each dictionary contains information on a single star system. The first item, at index 0, is the starting system, and the final destination is the last system in the list. Make any references to the list as the "plot" or "course": {converted_plot}'


    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=[
        {
            "role":"system",
            "content": PROMPT
        },
        {
            "role":"user",
            "content": question
        }
    ],
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )

    print(f'\nplotted reponse: {response}')

    return response.choices[0].message.content

def generic_answer(messages):

    # TODO: Add a prompt that course could not be found

    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message.content

def synthesize_answer(question, info):
        
    PROMPT = f'You are an friendly astro droid from the Star Wars universe. Fulfill navigation queries and general star system related questions for your master pilot using the following information: {info}'

    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=[
                  {
            "role":"system",
            "content": PROMPT
        },
        {
            "role":"user",
            "content": question
        }  
        ],
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].message.content
def is_asking_for_a_plot(question)-> bool:

    PROMPT = f'You are a navigation subprocessing unit. Determine if the user is asking for directions, a hyperspace plot course, or information from a list of star systems. Respond with only "True" or "False".'

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
        {
            "role":"system",
            "content": PROMPT
        },
        {
            "role":"user",
            "content": question
        }
    ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.0,
    )

    print(f'\nIs asking for a plot question reponse: {response}')

    answer = (response.choices[0].message.content)
    is_true = answer.lower() in ["true", "t", "yes", "y"]
    return is_true

def is_asking_about_a_system(question)-> bool:

    PROMPT = f'You are a data subprocessing unit. Determine if the user is asking for information regarding a single planet or star system from the Star Wars universe. Respond with only "True" or "False". Valid questions include "Where is Tatooine?" or "Tell me about Corsucant"'

    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
        {
            "role":"system",
            "content": PROMPT
        },
        {
            "role":"user",
            "content": question
        }
    ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.0,
    )

    print(f'\nIs asking for a system question reponse: {response}')

    answer = (response.choices[0].message.content)
    is_true = answer.lower() in ["true", "t", "yes", "y"]
    return is_true

def get_plot_answer(question):
    # Attempt to return DB vetted shorted path plot
    try:
        plot = get_plot(question)
    except InvalidStartLocation as e:
        return f"I'm afraid {e} is an uncharted or unknown system. Could you please rephrase your question with known origin?", None
    except InvalidEndLocation as e:
        return f"I'm afraid {e} is an uncharted or unknown system. Could you please rephrase your question with known destination?", None
   
    if plot == [] or plot is None:
        print("No plot data available for that query. Responding generically...")
        # TODO: Prepend with fact that plot couldn't be made
        return generic_answer(question), None
    
    print(f'\nFirst plot data: {plot[0]}')
    print(f'\njumps in plot returned: {len(plot)}')
    return plotted_answer(plot, question), plot

def extract_single_location(sentence)->str:

    prompt = f'You are a navigation droid from the Star Wars universe. Extract the name of the main star system of interest from a sentence and return just the came, like "Alderaan".'

    response = CLIENT.chat.completions.create(
    model="gpt-3.5-turbo", 
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

def get_system_answer(question):
    system_name = extract_single_location(question)
    if system_name is None or system_name == "":
        return generic_answer(question), None
    system = get_system_info(system_name)
    if system is None:
        return generic_answer(question), None
    return synthesize_answer(question, system), None

def ask(question: str, messages):

    request_plot = is_asking_for_a_plot(question)
    print(f'Is asking for a plot: {request_plot}')
    if request_plot is True:
        return get_plot_answer(question)
    request_system_info = is_asking_about_a_system(question)
    print(f'Is asking for system info: {request_system_info}')
    if request_system_info is True:
        return get_system_answer(question)
    return generic_answer(question, messages), None


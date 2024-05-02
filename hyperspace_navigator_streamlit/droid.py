from openai import OpenAI
from plotter import get_plot, InvalidEndLocation, InvalidStartLocation
from secrets_util import OPENAI_KEY

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

def ask(question: str, messages):

    # Attempt to return DB vetted shorted path plot
    try:
        plot = get_plot(question)
    except InvalidStartLocation as e:
        return f"I'm afraid {e} is an uncharted or unknown system. Could you please rephrase your question with known origin?"
    except InvalidEndLocation as e:
        return f"I'm afraid {e} is an uncharted or unknown system. Could you please rephrase your question with known destination?"
   
    if plot == [] or plot is None:
        print("No plot data available for that query. Responding generically...")
        # TODO: Prepend with fact that plot couldn't be made
        return generic_answer(messages), None
    
    print(f'\nFirst plot data: {plot[0]}')
    print(f'\njumps in plot returned: {len(plot)}')
    return plotted_answer(plot, question), plot
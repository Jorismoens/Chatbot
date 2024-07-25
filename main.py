import json
from openai import OpenAI
from callWeather import get_temperature
from getRandomN import get_random_numbers
from tools import tryRandomNTool, temperatureTool

client = OpenAI()

tools = [
    tryRandomNTool,
    temperatureTool
]

headsOrTails = ("To decide what to eat tonight, we want to flip a coin. At heads we'll eat pizza, at tails a salad. "
                "What will we eat tonight?")
trump = "Who is Donald Trump?"
willItRain = "Is there a chance of rain today in Amsterdam?"
tempZimbabwe = "how hot is it in Zimbabwe today?"
bbqWeather = "Is today a good day for bbq'ing in Antarctica?"
whichMonth = "Based on the weather in New York, what month do you think it is?"

messages = [
    {"role": "system", "content": "You assist me with calling specific tools to retrieve the temperature or generate "
                                  "random numbers."},
    {"role": "user", "content": whichMonth}
]
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

tool_calls = completion.choices[0].message.tool_calls
if tool_calls:
    tool_name = tool_calls[0].function.name
    if tool_name == 'get_random_numbers':
        args = json.loads(tool_calls[0].function.arguments)
        observation = get_random_numbers(**args)

        messages.append({
            "role": "function",
            "name": tool_name,
            "content": observation
        })

        response_with_function_call = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        print(response_with_function_call.choices[0].message.content)

    elif tool_name == 'get_temperature':
        args = json.loads(tool_calls[0].function.arguments)
        observation = get_temperature(**args)

        messages.append({
            "role": "function",
            "name": tool_name,
            "content": observation
        })

        response_with_function_call = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        print(response_with_function_call.choices[0].message.content)

else:
    # Model did not identify a function to call, hand the response message to the user
    print(completion.choices[0].message.content)
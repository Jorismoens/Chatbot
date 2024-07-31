import json
import string

from openai import OpenAI
from openai.types.chat import ChatCompletion

from src.tools.callWeather import get_temperature
from src.tools.getRandomN import get_random_numbers


def handle_tool_response(client: OpenAI, completion: ChatCompletion, messages: list[dict[str, str]]) -> string:

    # If the model decided to use any tools it will provide its choices in tool_calls. From this we call the correct
    # function corresponding to the name chosen by the model and put in the arguments that the model came up with.
    tool_calls = completion.choices[0].message.tool_calls

    if tool_calls:
        tool_name = tool_calls[0].function.name
        if tool_name == 'get_random_numbers':
            args = json.loads(tool_calls[0].function.arguments)

            # Call the actual tool with the arguments given by the model
            observation = get_random_numbers(**args)

            # Hand the function result back to the model
            messages.append({
                "role": "function",
                "name": tool_name,
                "content": observation
            })

            response_with_function_call = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            # The model reacts to the function result and gives a message back to the user
            return response_with_function_call.choices[0].message.content

        elif tool_name == 'get_temperature':
            args = json.loads(tool_calls[0].function.arguments)

            # Call the actual tool with the arguments given by the model
            observation = get_temperature(**args)

            # Hand the function result back to the model
            messages.append({
                "role": "function",
                "name": tool_name,
                "content": observation
            })

            response_with_function_call = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            # The model reacts to the function result and gives a message back to the user
            return response_with_function_call.choices[0].message.content

        else:
            return "error: function call defined by model does not exist"

    # Model did not identify a function to call, hand the response message to the user
    return completion.choices[0].message.content

import json
import string

from openai import OpenAI
from openai.types.chat import ChatCompletion

from src.tools.callWeather import get_temperature
from src.tools.getRandomN import get_random_numbers


def handle_tool_response(client: OpenAI, completion: ChatCompletion, messages: list[dict[str, str]]) -> string:
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

            return response_with_function_call.choices[0].message.content

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

            return response_with_function_call.choices[0].message.content

        else:
            return "error: function call defined by model does not exist"

    # Model did not identify a function to call, hand the response message to the user
    return completion.choices[0].message.content

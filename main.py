from openai import OpenAI

from completeFunctionCall import handle_tool_response
from prompts import PROMPTS
from tools import tryRandomNTool, temperatureTool

client = OpenAI()

tools = [
    tryRandomNTool,
    temperatureTool
]

messages = [
    {"role": "system", "content": "You assist me with calling specific tools to retrieve the temperature or generate "
                                  "random numbers."},
    {"role": "user", "content": PROMPTS["bbqWeather"]}
]
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

print(handle_tool_response(client, completion, messages))

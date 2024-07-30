import string
from openai import OpenAI
from src.handleToolResponse import handle_tool_response


def callAsistantWithTools(tools, role: string, prompt: string) -> string:
    messages = [
        {"role": "system",
         "content": role},
        {"role": "user", "content": prompt}
    ]
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    return handle_tool_response(client, completion, messages)

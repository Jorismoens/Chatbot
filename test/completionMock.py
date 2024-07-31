from typing import Literal


class MockFunction:
    arguments: list[object]
    name: str

    def __init__(self, arguments, name: str):
        self.arguments = arguments
        self.name = name


class MockToolCall:
    type: Literal['function', 'other']
    function: MockFunction

    def __init__(self, function: MockFunction, type):
        self.function: MockFunction = function
        self.type = type


class MockMessage:
    tool_calls: list[MockToolCall]
    content: str
    role: str

    def __init__(self, content, tool_calls: list[MockToolCall]):
        self.role = 'assistant'
        self.content = content
        self.tool_calls = tool_calls


class MockChoice:
    message: MockMessage

    def __init__(self, message):
        self.message = message


class MockCompletion:
    choices: list[MockChoice]

    def __init__(self, choices: list[MockChoice]):
        self.choices = choices

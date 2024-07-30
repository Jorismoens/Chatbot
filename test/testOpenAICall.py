import unittest
from typing import Literal
from unittest.mock import patch, call

from src.callAsistant import callAsistantWithTools
from src.tools.toolSchemas import randomNumbersTool


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
    content: object  # TODO
    role: str

    def __init__(self, content, tool_calls: list[MockToolCall]):
        self.role = 'assistant'
        self.content = content
        self.tool_calls = tool_calls


class MockChoice:
    message: object  # TODO

    def __init__(self, message):
        self.message = message


class MockCompletion:
    choices: list[MockChoice]

    def __init__(self, choices: list[MockChoice]):
        self.choices = choices


class TestOpenAICall(unittest.TestCase):

    @patch('openai.resources.chat.completions.Completions.create')
    def test_completions_api(self, mock_completions):
        # Ask a simple question, the assistant does not provide a tool. Check that the message is given back.

        # Define the mock response using custom classes
        response_content = "Hello, I'm doing well!"
        mock_message = MockMessage(content=response_content, tool_calls=[])
        mock_choice = MockChoice(message=mock_message)
        mock_response = MockCompletion(choices=[mock_choice])
        mock_completions.return_value = mock_response

        actual_response = callAsistantWithTools(tools=[], prompt="Hi chatbot, how are you?",
                                                role="You're a helpful assistant")

        mock_completions.assert_called_once_with(model='gpt-4o-mini',
                                                 messages=[{'role': 'system', 'content': "You're a helpful assistant"},
                                                           {'role': 'user', 'content': 'Hi chatbot, how are you?'}],
                                                 tools=[], tool_choice='auto')
        self.assertEqual(actual_response, response_content)

    @patch('src.handleToolResponse.get_random_numbers')
    @patch('openai.resources.chat.completions.Completions.create')
    def test_completions_api_random_number_tool(self, mock_completions, mock_random_numbers):
        # Define the mock response using custom classes
        response_content = ""
        mock_function = MockFunction(arguments='{"min":1,"max":6, "count": 5}', name='get_random_numbers')
        mock_tool_call = MockToolCall(function=mock_function, type='function')
        mock_message = MockMessage(content=response_content, tool_calls=[mock_tool_call])
        mock_choice = MockChoice(message=mock_message)
        mock_response = MockCompletion(choices=[mock_choice])
        mock_completions.return_value = mock_response

        mock_random_numbers.return_value = '{"random numbers": [1, 2, 3, 4, 5]}'

        actual_response = callAsistantWithTools(tools=[randomNumbersTool], prompt="Hi chatbot, how are you?",
                                                role="You're a helpful assistant")

        mock_completions.assert_called()

        self.assertEqual(actual_response, response_content)
        mock_random_numbers.assert_called_once_with(min=1, max=6, count=5)

    # Test with non defined function schema
    @patch('openai.resources.chat.completions.Completions.create')
    def test_completions_api_undefined_function(self, mock_completions):
        # Define the mock response using custom classes
        response_content = "call this non-existing function"
        mock_function = MockFunction(arguments=[], name='non-existing_function')
        mock_tool_call = MockToolCall(function=mock_function, type='function')
        mock_message = MockMessage(content=response_content, tool_calls=[mock_tool_call])
        mock_choice = MockChoice(message=mock_message)
        mock_response = MockCompletion(choices=[mock_choice])
        mock_completions.return_value = mock_response


        actual_response = callAsistantWithTools(tools=[randomNumbersTool], prompt="Hi chatbot, how are you?",
                                                role="You're a helpful assistant")

        mock_completions.assert_called()

        self.assertEqual(actual_response, "error: function call defined by model does not exist")

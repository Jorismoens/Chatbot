import json
import unittest
from unittest.mock import patch, Mock

from src.tools.getRandomN import get_random_numbers


class TestHelperFunctions(unittest.TestCase):

    # Happy flow
    @patch('requests.get')
    def test_get_random_numbers(self, mock_get):
        # Mock the API request and response
        mock_response = Mock()
        response_list = [22, 5, 135]
        response_dict = {
            "random numbers": response_list}
        response_json = json.dumps(response_dict)
        mock_response.json.return_value = response_list
        mock_get.return_value = mock_response

        random_numbers = get_random_numbers(0, 200, 3)
        mock_get.assert_called_once_with("http://www.randomnumberapi.com/api/v1.0/random",
                                         params={'min': 0, 'max': 200, 'count': 3})
        self.assertEqual(random_numbers, response_json)

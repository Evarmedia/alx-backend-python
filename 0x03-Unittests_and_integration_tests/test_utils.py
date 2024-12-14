#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function
    """
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Parameterized test for access_nested_map function.
        
        :param nested_map: Input nested map
        :param path: Path to access in the nested map
        :param expected: Expected return value
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """
        Parameterized test for access_nested_map function exceptions.
        
        :param nested_map: Input nested map
        :param path: Path to access in the nested map
        :param expected_key: Expected key in the exception message
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        
        # Check that the exception message contains the expected key
        self.assertEqual(str(context.exception), repr(expected_key))

class TestGetJson(unittest.TestCase):
    """
    Unit tests for the get_json function with mocked HTTP requests
    """
    
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test get_json function with mocked requests.get
        
        :param test_url: URL to mock
        :param test_payload: Expected payload to be returned
        """
        # Create a mock response object with a json method that returns test_payload
        with patch('requests.get') as mock_get:
            # Configure the mock to return a mock response with the specified json
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response
            
            # Call the function being tested
            result = get_json(test_url)
            
            # Assert that requests.get was called once with the correct URL
            mock_get.assert_called_once_with(test_url)
            
            # Assert that the returned result matches the test payload
            self.assertEqual(result, test_payload)

if __name__ == '__main__':
    unittest.main()
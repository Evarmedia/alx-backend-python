#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from utils import memoize
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map
from utils import get_json

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
        # Use patch as a context manager to mock requests.get
        with patch('requests.get') as mock_get:
            # Configure the mock response
            mock_get.return_value.json.return_value = test_payload
            
            # Call the function being tested
            result = get_json(test_url)
            
            # Assert that requests.get was called exactly once with the correct URL
            mock_get.assert_called_once_with(test_url)
            
            # Assert that the returned result matches the test payload
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """
    Unit tests for the memoize decorator
    """
    
    def test_memoize(self):
        """
        Test that the memoize decorator caches method results
        and calls the original method only once
        """
        class TestClass:
            def a_method(self):
                return 42
            
            @memoize
            def a_property(self):
                return self.a_method()
        
        # Create an instance of the test class
        test_obj = TestClass()
        
        # Mock the a_method
        with patch.object(test_obj, 'a_method') as mock_method:
            # Configure the mock method to return 42
            mock_method.return_value = 42
            
            # First call to a_property
            result1 = test_obj.a_property
            
            # Second call to a_property
            result2 = test_obj.a_property
            
            # Assert that a_method was called only once
            mock_method.assert_called_once()
            
            # Assert that both calls return the same result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

if __name__ == '__main__':
    unittest.main()
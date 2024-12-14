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

if __name__ == '__main__':
    unittest.main()
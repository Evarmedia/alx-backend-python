#!/usr/bin/python3
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

if __name__ == '__main__':
    unittest.main()
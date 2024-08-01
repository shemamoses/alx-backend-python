#!/usr/bin/env python3
'''
TestAccessNestedMap class that inherits from unittest.TestCase
'''
import unittest
from unittest.mock import Mock
from parameterized import parameterized
from typing import Mapping, Sequence, Union, Any
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    '''
    first test for utils.access_nested_map
    '''

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence,
            result: Union[Mapping, int]):
        '''
        Test access nested map
        '''
        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({}, ["a"]),
        ({"a": 1}, ["a", "b"])
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence):
        '''
        tests for errors raised by access_nested_map
        '''
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''
    Tests the utils.get_json func
    '''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @unittest.mock.patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Mapping, mock_get):
        '''
        tests get_json method with different urls
        '''
        my_mock = Mock()
        my_mock.json.return_value = test_payload
        mock_get.return_value = my_mock
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    '''
    tests utils.memoize decorator
    '''

    def test_memoize(self):
        '''
        test memoization decorator
        '''
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with unittest.mock.patch.object(TestClass, 'a_method') as mock_mthd:
            test = TestClass()
            test.a_property()
            test.a_property()
            mock_mthd.assert_called_once()

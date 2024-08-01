#!/usr/bin/env python3
'''
Testing client file methods defined in the GithubOrgClient class
'''
from client import GithubOrgClient, get_json
import utils
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from typing import Mapping, List
import unittest
from unittest.mock import Mock, PropertyMock, patch


class TestGithubOrgClient(unittest.TestCase):
    '''
    tests client.GithubOrgClient
    '''

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, org: str, mock_get):
        '''
        test that GithubOrgClient.org returns the correct value.
        '''
        client_test = GithubOrgClient(org)
        client_test.org()
        mock_get.assert_called_once_with(
            "https://api.github.com/orgs/{org}".format(org=org)
        )

    @patch(
        'client.GithubOrgClient.org',
        new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        '''
        unit-test GithubOrgClient._public_repos_url
        '''
        repo_url = GithubOrgClient("google")
        mock_resp = {"repos_url": "https://api.github.com/orgs/"}
        mock_org.return_value = mock_resp
        self.assertEqual(repo_url._public_repos_url, mock_resp['repos_url'])

    @patch('client.get_json')
    def test_public_repos(self, mock_get):
        '''
        unit-test GithubOrgClient.public_repos
        '''
        mock_payload = [{"name": "google"},
                        {"name": "microsoft"},
                        {"name": "excel"}]
        mock_url = "https://api.github.com/orgs/test"
        mock_get.return_value = mock_payload

        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock) as mock_repo_url:

            mock_repo_url.return_value = mock_url
            test_client = GithubOrgClient("google")

            self.assertEqual(
                test_client.public_repos(),
                [i['name'] for i in mock_payload])

            mock_repo_url.assert_called_once()
            mock_get.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self,
                         repo: Mapping,
                         license_key: str,
                         expected: bool):
        '''
        unit-test GithubOrgClient.has_license
        '''
        test_license = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(test_license, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''
    Test the GithubOrgClient.public_repos method in an integration test
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Sets up class for integration testing
        '''
        cls.get_patcher = patch('requests.get',
                                side_effect=cls.side_effect,
                                return_value=None)
        cls.mock = cls.get_patcher.start()

    @classmethod
    def side_effect(cls, url: str):
        '''
        Selects data to return based on given url
        '''
        my_mock = Mock()
        if url.endswith("/google"):
            my_mock.json.return_value = cls.org_payload
            return my_mock
        elif url.endswith("/google/repos"):
            my_mock.json.return_value = cls.repos_payload
            return my_mock
        else:
            return DEFAULT

    def test_public_repos(self) -> None:
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

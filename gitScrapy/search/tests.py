from django.test import TestCase
from django.conf import settings
from unittest.mock import patch

from .utils import get_query, url_exists, process_response


class LogicTestCase(TestCase):
    url = settings.GITHUB_API_URL

    def test_returns_true_if_url_found(self):
        with patch('requests.get') as mock_request:
            mock_request.return_value.status_code = 200

            self.assertTrue(url_exists(self.url))

    def test_equal_query_result(self):
        result = get_query('vova')

        for line in result.split("\n"):
            if not line.strip():
                continue
            if line.strip() == 'user(login: "vova") {':
                string = 'user(login: "vova") {'
                break

        self.assertEqual(string[5:-3], 'login: "vova"')

    def test_response_content_is_empty(self):
        response = process_response('vovovoovo')
        response = response.json()

        if response['errors']:
            flag = True

        self.assertEqual(flag, True)

    def test_response_content(self):
        response = process_response('trco')
        response = response.json()
        valid_photo_url = 'https://avatars.githubusercontent.com/u/33464584?'\
                          'u=e33dfcb4cdbd62ae77880036ef7146840d8339c0&v=4'
        repos = []

        r = response.pop('data')
        r = r.pop('user')
        full_name = r['name']
        avatar = r['avatarUrl']
        for el in r['repositories'].pop('nodes'):
            repos.append(el['name'])

        self.assertEqual(full_name, 'Uroš Trstenjak')
        self.assertEqual(
                        avatar, valid_photo_url)
        self.assertEqual(len(repos), 28)

    def test_user_has_not_fullname(self):
        response = process_response('aaaaaaaaaaaaa')
        response = response.json()

        r = response.pop('data')
        r = r.pop('user')

        non_user = r['name']

        self.assertIsNone(non_user)

    def test_user_has_not_repos(self):
        response = process_response('bolvanka')
        response = response.json()
        repos = []

        r = response.pop('data')
        r = r.pop('user')
        for el in r['repositories'].pop('nodes'):
            repos.append(el['name'])

        self.assertEqual(len(repos), 0)

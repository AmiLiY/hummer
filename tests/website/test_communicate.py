import unittest

from website.communicate import Communicator


class CommunicatorTestCase(unittest.TestCase):
    def test_login(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        cookies = client.login(data)
        print(cookies)

    def test_logout(self):
        cookies = {'sessionid': 't53iaqdoqyw5rx9f9i8yjv0xjsb04v67'}
        client = Communicator(cookies=cookies)
        cookies = client.logout()
        print(cookies)

    def test_is_authenticated(self):
        cookies = {'sessionid': 'fw7a2cn2ybklvbcszv9qj6316ass7c8'}
        client = Communicator(cookies=cookies)
        ok, username = client.is_authenticated()
        print(ok)
        print(username)

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

    def test_registry(self):
        data = {
            'username': 'test',
            'password': 'test123',
            'email': 'test@hummer.com',
            'is_staff': False,
            'is_active': True
        }
        client = Communicator()
        cookies = client.registry(data)
        print(cookies)

    def test_project_lists(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)
        projects = client.project_lists()
        print(projects)

    def test_delete_project(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)
        client.delete_project(11)

    def test_delete_image(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)
        client.delete_image(1, 2)

    def test_create_image(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)
        params = {
            'name': 'logtest',
            'version': '0.1',
            'desc': 'this is for test.',
            'is_public': 'false',
            'is_image': '0',
            'dockerfile': 'Dockerfile'
        }
        buildfile = '/home/wangtao/hummer-test/buildfiles/logtest/logtest.tar'
        ok = client.create_image(2, params, buildfile)
        print(ok)

    def test_get_image_username(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        res = client.get_image_username(project_id=2, image_id=12)
        print(res)

    def test_get_image(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        res = client.get_image(project_id=2, image_id=12)
        print(res)

    def test_create_application(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        data = {
            'image': 1,
            'name': 'test-app',
            'replicas': 1,
            'resource_limit': 1,
            'is_public': True,
            'session_affinity': False,
            'ports': [{'name': 'http', 'port': 80, 'protocol': 'TCP'}],
        }
        client.create_application(1, data)

    def test_get_application_username(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        res = client.get_application_username(project_id=2, application_id=5)
        print(res)

    def test_upload_to_volume(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        files = "/home/wangtao/hummer-test/buildfiles/myubuntu/myubuntu.tar"
        client.upload_to_volume(1, 5, files)

    def test_clear_volume(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        client.clear_volume(1, 5)

    def test_get_pod_logs(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        res = client.get_pod_logs(1, "project0-nginx-test-n9oky", 20)
        print(res)

    def test_clone_public_image(self):
        client = Communicator()
        data = {
            'username': 'user',
            'password': 'user123'
        }
        client.login(data)

        data = {
            'pid': 1,
            'name': 'myubuntu',
            'version': '14.04'
        }
        res = client.clone_public_image(12, data)
        print(res)

    def test_delete_resource_module(self):
        client = Communicator()
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        client.login(data)

        res = client.delete_resource_module(2)
        print(res)

    def test_list_members(self):
        client = Communicator()
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        client.login(data)

        res = client.list_members(2)
        print(res)

    def test_add_members(self):
        client = Communicator()
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        client.login(data)

        res = client.add_members(2, [1, 2])
        print(res)

    def test_remove_members(self):
        client = Communicator()
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        client.login(data)

        res = client.remove_members(2, [1, 2])
        print(res)

import json
import requests
import logging

from backend.kubernetes.namespace import Namespace
from backend.kubernetes.replicationcontroller import Controller
from backend.kubernetes.service import Service
from backend.kubernetes.volume import PersistentVolume, PersistentVolumeClaim
from backend.kubernetes.autoscaler import AutoScaler

logger = logging.getLogger('hummer')


class KubeClient(object):
    """
    Kubernetes simple python client.
    API: http://kubernetes.io/third_party/swagger-ui/
    """
    _base_url = None
    def __init__(self, base_url):
        self._base_url = self.add_slash(base_url)

    @classmethod
    def add_slash(self, url):
        """
        Promote that the base url ends with '/'.
        """
        if url.endswith('/'):
            return url
        return url + '/'

    @property
    def base_url(self):
        return self._base_url

    def _send_request(self, method, path, label=None, query=None, body=None):
        """
        Send requests to k8s server and get the response.
        Returns a response dict.

        Parameters:
        query: str, "app=name"
        """
        url = self._base_url + path
        if label:
            url = '{}?labelSelector={}'.format(url, label)
        if query:
            url = url + '?' + query
        kwargs = {}
        if body:
            kwargs['data'] = json.dumps(body)

        try:
            res = getattr(requests, method.lower())(url, **kwargs)
        except Exception as error:
            logger.error(error)
            logger.error(res)
            return None

        try:
            response = json.loads(res.text)
            return response
        except Exception as error:
            return res.text

    def list_nodes(self):
        """
        List all nodes.
        """
        res = self._send_request('GET', 'nodes')
        nodes = []
        for item in res.get('items'):
            nodes.append(item['metadata']['name'])
        return nodes

    def list_namespces(self):
        """
        List all namespaces.
        """
        res = self._send_request('GET', 'namespaces')
        namespaces = []
        for item in res.get('items'):
            namespaces.append(item['metadata']['name'])
        return namespaces

    def create_namespace(self, name):
        """
        Create namespace called name.
        """
        namespace = Namespace(name)

        response = self._send_request('POST', 'namespaces', body=namespace.body)
        return self._is_creating_deleting_successful(response)

    def delete_namespace(self, name):
        """
        Delete namespace called name.
        """
        response = self._send_request('DELETE', 'namespaces/{}'.format(name))
        return self._is_creating_deleting_successful(response)

    def create_persistentvolume(self, namespace, name, capacity, nfs_path,
        nfs_server):
        """
        Create persistentvolume called namespace-name.
        """
        volume_name = namespace + '-' + name
        volume = PersistentVolume(volume_name, capacity, nfs_path, nfs_server)
        response = self._send_request('POST', 'persistentvolumes',
            body=volume.body)
        return self._is_creating_deleting_successful(response)

    def delete_persistentvolume(self, namespace, name):
        """
        Delete persistentvolume called namespace-name.
        """
        volume_name = namespace + '-' + name
        response = self._send_request('DELETE', 'persistentvolumes/{}'.format(
            volume_name))
        return self._is_creating_deleting_successful(response)

    def create_persistentvolumeclaim(self, namespace, name, capacity):
        """
        Create persistentvolumeclaim called name.
        """
        volume_name = namespace + '-' + name
        volumeclaim = PersistentVolumeClaim(volume_name, capacity)
        response = self._send_request('POST',
            'namespaces/{}/persistentvolumeclaims'.format(namespace),
            body=volumeclaim.body)
        return self._is_creating_deleting_successful(response)

    def delete_persistentvolumeclaim(self, namespace, name):
        """
        Delete persistentvolumeclaim called name.
        """
        volume_name = namespace + '-' + name
        response = self._send_request('DELETE',
            'namespaces/{}/persistentvolumeclaims/{}'.format(namespace,
                volume_name))
        return self._is_creating_deleting_successful(response)

    def list_controllers(self, namespace):
        """
        List all replicationcontroller in the namespace.
        """
        path = 'namespaces/{}/replicationcontrollers'.format(namespace)
        res = self._send_request('GET', path)
        controllers = []
        for item in res.get('items'):
            controllers.append(item['metadata']['name'])
        return controllers

    def create_controller(self, namespace, name, image_name, cpu, memory,
        replicas=1, tcp_ports=None, udp_ports=None, commands=None, args=None,
        envs=None, volumes=None):
        """
        Create a replicationcontroller.
        """
        controller = Controller(name, image_name, cpu, memory, replicas,
            tcp_ports, udp_ports, commands, args, envs, volumes)
        path = 'namespaces/{}/replicationcontrollers'.format(namespace)

        # logger.debug(controller.body)
        response = self._send_request('POST', path, body=controller.body)
        return self._is_creating_deleting_successful(response)

    def delete_controller(self, namespace, name):
        """
        Delete a replicationcontroller.
        """
        path = 'namespaces/{}/replicationcontrollers/{}'.format(namespace, name)
        response = self._send_request('DELETE', path)
        return self._is_creating_deleting_successful(response)

    def list_pods(self, namespace, label=None):
        """
        List pods by label.

        Parameters:
        label: str, "app=name"
        """
        path = 'namespaces/{}/pods/'.format(namespace)
        response = self._send_request('GET', path, label=label)
        # logger.debug(response)
        pods = []
        for item in response.get('items'):
            pods.append(item['metadata']['name'])
        return pods

    def list_host_ips(self, namespace, label=None):
        """
        List all host ips for a controller.

        Parameters:
        label: str, "app=name"
        """
        path = 'namespaces/{}/pods/'.format(namespace)
        response = self._send_request('GET', path, label=label)
        # logger.debug(response)
        hosts = set()
        for pod in response.get('items', []):
            hosts.add(pod['spec']['nodeName'])
        return list(hosts)

    def delete_pod(self, namespace, name):
        """
        Delete a pod.
        """
        path = 'namespaces/{}/pods/{}'.format(namespace, name)
        response = self._send_request('DELETE', path)
        return self._is_creating_deleting_successful(response)

    def list_services(self, namespace):
        """
        List all services in the namespace.
        """
        path = 'namespaces/{}/services'.format(namespace)
        res = self._send_request('GET', path)
        services = []
        for item in res.get('items'):
            services.append(item['metadata']['name'])
        return services

    def create_service(self, namespace, name, tcp_ports=None, udp_ports=None,
        is_public=False, session_affinity=False):
        """
        Create a service in namespace.
        """
        service = Service(name, tcp_ports, udp_ports, is_public,
            session_affinity)
        path = 'namespaces/{}/services'.format(namespace)

        # logger.debug(service.body)
        response = self._send_request('POST', path, body=service.body)
        return self._is_creating_deleting_successful(response)

    def delete_service(self, namespace, name):
        """
        Delete a service.
        """
        path = 'namespaces/{}/services/{}'.format(namespace, name)
        response = self._send_request('DELETE', path)
        return self._is_creating_deleting_successful(response)

    def get_service_details(self, namespace, name):
        """
        Get the details of a service.
        """
        path = 'namespaces/{}/services/{}'.format(namespace, name)
        response = self._send_request('GET', path)
        return response

    def _is_creating_deleting_successful(self, response):
        """
        Check the response to determinate whether creating and resource
        successfully.
        """
        status = response['status']
        if isinstance(status, str) and status == 'Failure':
            logger.debug(response['message'])
            return False
        return True

    def get_logs_of_pod(self, namespace, pod_name, tail_line):
        """
        Return the tail tail_line lines of logs of pod named pod_name.
        """
        path = 'namespaces/{}/pods/{}/log'.format(namespace, pod_name)
        query = "tailLines=" + str(tail_line)
        response = self._send_request('GET', path, query=query)
        return response.split('\n')

    def create_autoscaler(self, namespace, name, minReplicas=-1, maxReplicas=-1,
        cpu_target=-1):
        """
        Create an autoscaler name in namespace namespace.
        """
        scaler = AutoScaler(name, minReplicas, maxReplicas, cpu_target)
        path = 'namespaces/{}/horizontalpodautoscalers'.format(namespace)

        # logger.debug(scaler.body)
        response = self._send_request('POST', path, body=scaler.body)
        return self._is_creating_deleting_successful(response)

    def delete_autoscaler(self, namespace, name):
        """
        Delete the autoscaler name.
        """
        path = 'namespaces/{}/horizontalpodautoscalers/{}'.format(namespace,
            name)
        response = self._send_request('DELETE', path)
        return self._is_creating_deleting_successful(response)

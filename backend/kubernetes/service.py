

class Service(object):
    """
    Kubernetes service, each application has a service.

    Parameters:
    name: application name.
    tcp_ports: the TCP ports of the service.
    udp_ports: the UDP ports of the service.
    is_public: boolean.
    """
    _body = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": None,
            "labels": {
                "app": None
            }
        },
        "spec": {
            "selector": {
                "app": None
            },
            "ports": [],
            "type": "ClusterIP",
            "sessionAffinity": "None"
        }
    }

    def __init__(self, name, tcp_ports=None, udp_ports=None, is_public=False,
        session_affinity=False):
        self._body['metadata']['name'] = name
        self._body['metadata']['labels']['app'] = name
        self._body['spec']['selector']['app'] = name

        if tcp_ports:
            self.set_ports("TCP", tcp_ports)
        if udp_ports:
            self.set_ports("UDP", udp_ports)

        if is_public:
            self._body['spec']['type'] = "NodePort"
        if session_affinity:
            self._body['spec']['sessionAffinity'] = "ClientIP"

    def set_ports(self, type, ports):
        """
        Open port for the service.
        """
        for port in ports:
            self._body['spec']['ports'].append({
                'protocol': type,
                'port': port})

    @property
    def body(self):
        return self._body

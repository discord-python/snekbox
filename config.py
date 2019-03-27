import os

import docker
from docker.errors import NotFound


def autodiscover():
    """Search for the snekbox container and return its IPv4 address."""

    container_names = ["rmq", "pdrmq", "snekbox_pdrmq_1"]

    client = docker.from_env()
    for name in container_names:
        try:
            container = client.containers.get(name)
            if container.status == "running":
                host = list(container.attrs.get('NetworkSettings').get('Networks').values())
                host = host[0]['IPAddress']
                return host
        except NotFound:
            continue
        except Exception:
            pass

    return '127.0.0.1'


USERNAME = os.environ.get('RMQ_USERNAME', 'guest')
PASSWORD = os.environ.get('RMQ_PASSWORD', 'guest')
HOST = os.environ.get('RMQ_HOST', autodiscover())
PORT = 5672
QUEUE = 'input'
EXCHANGE = QUEUE
ROUTING_KEY = QUEUE
EXCHANGE_TYPE = 'direct'

from rcon.source import Client


def get_client(ip="127.0.0.1", port=25575, password="", timeout_duration=3):
    return Client(ip, port, passwd=password, timeout=timeout_duration)

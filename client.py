import tomllib

# from rcon.source import Client  # initial, using: https://pypi.org/project/rcon/
from rcon import Console

import logger

log = logger.get_logger(__name__)


# fetch config
def fetch_config():
    with open("config.toml", "rb") as file:
        data = tomllib.load(file)
    if data:
        return data
    log.error("Unable to read configuration file!")


CONFIG = fetch_config()


# ------------------------------------------------------------------------------
# Fallback
def send_command_fallback(command: str):
    con = Console(
        host=CONFIG["ip"],
        password=CONFIG["password"],
        port=CONFIG["port"],
        timeout=CONFIG["timeout_duration"]
    )
    res = con.command(command)
    con.close()

    log.debug(res)
    return res
# Initial RCON library wrapper:
# def get_client(ip="127.0.0.1", port=25575, password="", timeout_duration=3):
#     return Client(ip, port, passwd=password, timeout=timeout_duration)

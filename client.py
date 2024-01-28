import tomllib

from rcon import Console

import logger

log = logger.get_logger(__name__)


def fetch_config():
    log.info("Fetching configuration file")
    with open("config.toml", "rb") as file:
        data = tomllib.load(file)
    if data:
        return data
    log.error("Unable to read configuration file!")


# ------------------------------------------------------------------------------
# Fallback - for testing only
def send_command_fallback(command: str):
    log.info("Testing RCON connection")
    config = fetch_config()
    con = Console(
        host=config["ip"],
        password=config["password"],
        port=config["port"],
        timeout=config["timeout_duration"]
    )
    res = con.command(command)
    con.close()

    log.debug(res)
    return res


# ------------------------------------------------------------------------------
class Client:
    def __init__(self):
        log.info("Setting up RCON connection")
        config = fetch_config()
        self.CONSOLE = Console(
            host=config["ip"],
            password=config["password"],
            port=config["port"],
            timeout=config["timeout_duration"]
        )

    def close(self):
        log.info("Closing RCON connection")
        self.CONSOLE.close()

    # Admin Commands:

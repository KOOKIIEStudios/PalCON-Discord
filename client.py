import tomllib

from rcon import Console
from rcon.async_support import Console as AsyncConsole

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
# Synchronous implementation; manually starts and stops a connection with every command
class Client:
    def __init__(self):
        self.GENERIC_ERROR = "Unable to process your request (server did not respond)"
        log.info("Setting up RCON connection")
        self.CONFIG = fetch_config()

    def open(self):
        return Console(
            host=self.CONFIG["ip"],
            password=self.CONFIG["password"],
            port=self.CONFIG["port"],
            timeout=self.CONFIG["timeout_duration"]
        )

    # Admin Commands:
    def info(self):
        log.debug("Fetching server info")
        console = self.open()
        res = console.command("Info")
        console.close()
        return res if res else self.GENERIC_ERROR

    def save(self):
        log.debug("Saving world")
        console = self.open()
        res = console.command("Save")
        console.close()
        return res if res else self.GENERIC_ERROR
    
    def online(self):
        # Response is of format `name,playerid,steamid`
        log.debug("Fetching online players")
        console = self.open()
        res = console.command("ShowPlayers")
        console.close()

        players = []
        # format output
        if res:
            lines = res.split()[1:]
            buffer = ["## List of connected player names"]
            for line in lines:
                words = line.split(",")
                name = words[0]
                steam_id = words[2]
                players.append((name, steam_id))
                buffer.append(f"- {words[0]} (Steam ID: {words[2]})")
            output = "\n".join(buffer)
        else:
            output = self.GENERIC_ERROR

        return output, players

    def announce(self, message: str):
        log.debug("Broadcasting message to world")
        console = self.open()
        res = console.command(f"Broadcast {message}")
        console.close()
        # TODO: Consider reformatting server's response
        return res if res else self.GENERIC_ERROR

    def kick(self, steam_id: str):
        log.debug("Kicking player from server")
        console = self.open()
        res = console.command(f"KickPlayer {steam_id}")
        console.close()
        return res if res else self.GENERIC_ERROR

    def ban(self, steam_id: str):
        log.debug("Banning player from server")
        console = self.open()
        res = console.command(f"BanPlayer {steam_id}")
        console.close()
        return res if res else self.GENERIC_ERROR

    def shutdown(self, seconds: str, message: str):
        log.debug(f"Schedule server shutdown in {seconds} seconds")
        console = self.open()
        res = console.command(f"Shutdown {seconds} {message}")
        console.close()
        return res if res else self.GENERIC_ERROR

    def force_stop(self):
        log.debug(f"Terminating the server forcefully")
        console = self.open()
        res = console.command(f"DoExit")
        console.close()
        # TODO: Check if this is supposed to give a response (and alter accordingly)
        return res if res else self.GENERIC_ERROR


# ------------------------------------------------------------------------------
# Async implementation; connection remains open throughout lifetime
# This is listed as experimental on the library's docs, for use with Discord bots
# In my testing, it doesn't receive the correct number of bytes as of 28th Jan 2024
class AsyncClient:
    def __init__(self):
        self.GENERIC_ERROR = "Unable to process your request (server did not respond)"
        log.info("Setting up RCON connection")
        config = fetch_config()
        self.CONSOLE = AsyncConsole(
            host=config["ip"],
            password=config["password"],
            port=config["port"],
            timeout=config["timeout_duration"]
        )

    async def check_console_ready(self):
        if not self.CONSOLE.is_open():
            await self.CONSOLE.open()

    async def close(self):
        log.info("Closing RCON connection")
        await self.CONSOLE.close()

    # Admin Commands:
    async def info(self):
        await self.check_console_ready()
        res = await self.CONSOLE.command("Info")
        return res if res else self.GENERIC_ERROR

    async def save(self):
        await self.check_console_ready()
        res = await self.CONSOLE.command("Save")
        return res if res else self.GENERIC_ERROR

    async def online(self):
        # Response is of format `name,playerid,steamid`
        await self.check_console_ready()
        res = await self.CONSOLE.command("ShowPlayers")
        # TODO: REFORMAT INTO MORE READABLE OUTPUT
        return res if res else self.GENERIC_ERROR

    async def announce(self, message: str):
        await self.check_console_ready()
        res = await self.CONSOLE.command(f"Broadcast {message}")
        # TODO: Consider reformatting reply
        return res if res else self.GENERIC_ERROR

    async def kick(self, steam_id: str):
        await self.check_console_ready()
        res = await self.CONSOLE.command(f"KickPlayer {steam_id}")
        return res if res else self.GENERIC_ERROR

    async def ban(self, steam_id: str):
        await self.check_console_ready()
        res = await self.CONSOLE.command(f"BanPlayer {steam_id}")
        return res if res else self.GENERIC_ERROR

    async def shutdown(self, seconds: str, message: str):
        await self.check_console_ready()
        res = await self.CONSOLE.command(f"Shutdown {seconds} {message}")
        return res if res else self.GENERIC_ERROR

    async def force_stop(self):
        await self.check_console_ready()
        res = await self.CONSOLE.command(f"DoExit")
        return res if res else self.GENERIC_ERROR

import tomllib

from rcon import Console
from rcon.async_support import Console as AsyncConsole

from data import ServerInfo
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
    """
    This is only to manually check if the RCON side works, independently
    of the Discord bot. It is not and should not be called by the bot.
    """
    log.info("Testing RCON connection")
    config = fetch_config()
    log.debug(f'IP: {config["ip"]}, Port: {config["port"]}')
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


# Helper functions; RCON client output parsing --------------------------------
def get_indices_from_info(res: str) -> tuple[int, int, int]:
    version_number_start_index = -1
    version_number_end_index = -1
    name_index = -1
    for index, char in enumerate(res):
        if char == "[":
            version_number_start_index = index + 1
        if char == "]":
            version_number_end_index = index
            name_index = version_number_end_index + 2
            break

    return version_number_start_index, version_number_end_index, name_index


# ------------------------------------------------------------------------------
# Synchronous implementation; manually starts and stops a connection with every command
class Client:
    def __init__(self, config: dict = None):
        self.GENERIC_ERROR = "Unable to process your request (server did not respond)"
        log.info("Setting up RCON connection")
        if config:
            self.CONFIG = config
        else:
            self.CONFIG = fetch_config()

    def open(self) -> Console:
        return Console(
            host=self.CONFIG["ip"],
            password=self.CONFIG["password"],
            port=self.CONFIG["port"],
            timeout=self.CONFIG["timeout_duration"]
        )

    # Admin Commands:
    def info(self) -> tuple[ServerInfo | None, str]:
        """Returns the game server name and version number"""
        log.debug("Fetching server info")
        console = self.open()
        res = console.command("Info")
        console.close()

        server_info = None
        error_message = ""
        if res:
            version_start_index, version_end_index, name_index = get_indices_from_info(res)
            if version_start_index < 0 or version_end_index < 0 or name_index < 0:
                log.error("Unable to parse server info!")
                error_message = "Unable to process your request (server response in unexpected format)"
            else:
                server_info = ServerInfo(
                    version=res[version_start_index:version_end_index],
                    name=res[name_index:],
                )
        else:
            error_message = self.GENERIC_ERROR

        return server_info, error_message

    def save(self) -> str:
        log.debug("Saving world")
        console = self.open()
        res = console.command("Save")
        console.close()
        return res if res else self.GENERIC_ERROR
    
    def online(self) -> tuple[dict[str, str], str]:
        """Returns dict of online players, and error message (if any)
        { Key (Steam ID): Value (IGN) }
        """
        # Response is of format `name,playerid,steamid\n`
        log.debug("Fetching online players")
        console = self.open()
        res = console.command("ShowPlayers")
        console.close()

        players = {}
        error_message = ""
        # format output
        if res: # "name,playeruid,steamid\n" this is the header
            lines = res.split('\n')[1:-1] # remove the header and last elemement which is always an empty string
            log.debug(f'Lines: {lines}')
            for line in lines:
                log.debug(f'Line: {line}')
                words = line.split(",")
                if len(words) < 3:
                    log.error(f'Unable to parse player info for player, player is missing some information: {words}')
                    break

                ign = words[0]
                steam_id = words[2]

                if len(words) > 3:
                    log.debug(f'Ran into a player with more than 3 points of data during parsing: {words}')
                    # If the player name has a comma, the split will produce more than 3 words
                    ign = ",".join(words[0:-2])
                    steam_id = words[-1]

                players[steam_id] = ign
        else:
            error_message = self.GENERIC_ERROR

        return players, error_message

    def get_ign_from_steam_id(self, steam_id: str) -> str:
        """Fetches player name from Steam ID, if player is online"""
        players, _ = self.online()
        return players.get(steam_id, "")

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
        log.debug("Terminating the server forcefully")
        console = self.open()
        res = console.command("DoExit")
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
        res = await self.CONSOLE.command("DoExit")
        return res if res else self.GENERIC_ERROR

if __name__ == "__main__":
    client = Client()
    players, error = client.online()
    print(players)
    logger.shutdown_logger()

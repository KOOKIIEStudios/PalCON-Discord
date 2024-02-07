import asyncio
import tomllib

from rcon.source import rcon

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
async def send_command_fallback(command: str):
    """
    This is only to manually check if the RCON side works, independently
    of the Discord bot. It is not and should not be called by the bot.
    """
    config = fetch_config()
    log.debug(f'IP: {config["ip"]}, Port: {config["port"]}')

    res = await rcon(
        command,
        host=config["ip"],
        port=config["port"],
        passwd=config["password"],
        timeout=config["timeout_duration"],
        enforce_id=False,
    )

    log.debug(res)
    return res


# ------------------------------------------------------------------------------
# Asynchronous implementation
class Client:
    def __init__(self, config: dict = None):
        self.GENERIC_ERROR = "No response from server"

        if config:
            self.CONFIG = config
        else:
            self.CONFIG = fetch_config()

    async def run(self, command: str, *arguments: str) -> str:
        """Sends a command asynchronously"""
        return await rcon(
            command,
            *arguments,
            host=self.CONFIG["ip"],
            port=self.CONFIG["port"],
            passwd=self.CONFIG["password"],
            timeout=self.CONFIG["timeout_duration"],
            enforce_id=False,
        )

    @staticmethod
    def get_indices_from_info(res: str) -> tuple[int, int, int]:
        """Helper method for pre-processing game server info text"""
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

    # Non-admin commands:
    async def info(self) -> ServerInfo:
        """Returns the game server name and version number

        Raises:
            RuntimeError: No response from server but connection did not time out
            ValueError: Unexpected formatting from server output
        """
        log.debug("Fetching server info")
        res = await self.run("Info")

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        version_start_index, version_end_index, name_index = self.get_indices_from_info(res)
        if version_start_index < 0 or version_end_index < 0 or name_index < 0:
            log.error("Unable to parse server info!")
            raise ValueError("RCON server response in unexpected format")

        server_info = ServerInfo(
            version=res[version_start_index:version_end_index],
            name=res[name_index:],
        )

        return server_info

    async def online(self) -> tuple[dict[str, str], bool]:
        """Fetches a dictionary containing all currently connected players

        Returns:
            A dictionary mapping Steam ID to player name, for example:

            { Key (Steam ID): Value (IGN) }

            The second returned object is a boolean flag for whether any of the
            player information could not be parsed:
            False => all player's name and Steam ID could be detected
            True => one or more player's name and/or Steam ID could not be read

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        # Response is of format `<name>,<player id>,<steam id>\n`
        log.debug("Fetching online players")
        res = await self.run("ShowPlayers")

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        players = {}
        faulty = False
        # format output --------------------------------------------------------
        # first line: "name,playeruid,steamid\n"; last line is empty because of `\n`
        lines = res.split('\n')[1:-1]  # strip unnecessary lines
        log.debug(f'Lines: {lines}')
        for line in lines:
            log.debug(f'Line: {line}')
            words = line.split(",")
            if len(words) < 3:
                log.error(f'Unable to parse player info for player, player is missing some information: {words}')
                faulty = True
                break

            ign = words[0]
            steam_id = words[2]

            if len(words) > 3:
                log.debug(f'Ran into a player with more than 3 points of data during parsing: {words}')
                faulty = True
                # If the player name has a comma, the split will produce more than 3 words
                ign = ",".join(words[0:-2])
                steam_id = words[-1]

            players[steam_id] = ign

        return players, faulty

    # Admin Commands:
    async def save(self) -> str:
        """Issues command to save on the game server

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        log.debug("Saving world")
        res = await self.run("Save")

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        return res

    async def get_ign_from_steam_id(self, steam_id: str) -> str:
        """Fetches player name from Steam ID, if player is online

        Defaults to empty string, if name is not found

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        players, _ = await self.online()
        return players.get(steam_id, "")

    async def announce(self, message: str):
        """Sends an in-game announcement

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        log.debug("Broadcasting message to world")
        res = await self.run("Broadcast", message)

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        return res

    async def kick(self, steam_id: str):
        """Kicks a player from the game server

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        log.debug("Kicking player from server")
        res = await self.run("KickPlayer", steam_id)

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        return res

    async def ban(self, steam_id: str):
        """Bans a player from the game server

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        log.debug("Banning player from server")
        res = await self.run("BanPlayer", steam_id)

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        return res

    async def shutdown(self, seconds: str, message: str):
        """Issue a request to the game server to schedule an elegant shutdown

        Args:
            seconds: Number of seconds till shutdown
            message: Announcement to make in-game

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        log.debug(f"Schedule server shutdown in {seconds} seconds")
        res = await self.run("Shutdown", seconds, message)

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        return res

    async def force_stop(self):
        """Issue a request to forcefully terminate the game server

        Raises:
            RuntimeError: No response from server but connection did not time out
        """
        log.debug("Terminating the server forcefully")
        res = await self.run("DoExit")

        if not res:
            raise RuntimeError(self.GENERIC_ERROR)

        return res


if __name__ == "__main__":
    log.info("Testing RCON connection")

    log.info("Testing raw commands")
    log.info("Grabbing game server info")
    asyncio.run(send_command_fallback("Info"))

    log.info("Testing client wrapper using broadcasts")
    rcon_client = Client()
    asyncio.run(rcon_client.announce("This_is_an_announcement_with_no_spaces"))
    logger.shutdown_logger()

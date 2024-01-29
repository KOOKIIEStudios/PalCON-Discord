import sys

import discord
from discord import app_commands

from client import fetch_config, Client
from data import ServerInfo
import logger


config = fetch_config()
log = logger.get_logger(__name__)

STEAM_PROFILE_URL = "https://steamcommunity.com/profiles/{steam_id}/"


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(*args, **kwargs, intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        log.info("Bot is online!")


discord_client = DiscordClient()
tree = app_commands.CommandTree(discord_client)


# Bot helper functions ---------------------------------------------------------
def format_embed(embedded_message: discord.Embed) -> None:
    embedded_message.set_footer(text=config["embed_footer"])
    embedded_message.set_thumbnail(url=config["embed_thumbnail"])


# Start of Slash Commands ------------------------------------------------------
@tree.command(
    name="info",
    description="Get server information",
)
async def info(interaction: discord.Interaction):
    embed_message = None
    error = config["generic_bot_error"]
    try:
        rcon_client = Client(config=config)
        server_info, error_message = rcon_client.info()
        if server_info:
            embed_message = discord.Embed(
                title=server_info.name,
                colour=discord.Colour.blurple(),
                description=f"Version: {server_info.version}",
            )
            format_embed(embed_message)
        elif error_message:
            error = error_message
    except Exception as e:
        log.error(f"Exception occurred while executing command: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(error)


@tree.command(
    name="online",
    description="Get information about all online players",
)
async def online(interaction: discord.Interaction):
    embed_message = None
    try:
        rcon_client = Client(config=config)
        output, players = rcon_client.online()
        embed_message = discord.Embed(title="Players Online", colour=discord.Colour.blurple(), description=f"Player(s) Online: {len(players)}")
        format_embed(embed_message)

        # TODO: Add a pagination system for when there are a lot of players online
        list_of_players = ""
        for player in players:
            list_of_players += f"[{player[0]}]({STEAM_PROFILE_URL.format(steam_id=player[1])})\n"
        embed_message.add_field(name="Players", value=list_of_players, inline=False)
    except Exception as e:
        log.error(f"Exception occurred while executing command: {e}")
        output = "Unable to process your request (server did not respond)"

    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(output)


# End of Slash Commands --------------------------------------------------------
def main(discord_bot_token):
    if not config:
        logger.shutdown_logger()
        sys.exit(0)
    log.info("Configuration files loaded")

    log.info("Starting PalCON Discord Bot...")
    discord_client.run(discord_bot_token)


if __name__ == "__main__":
    main(config["discord_bot_token"])
    
    logger.shutdown_logger()
    sys.exit(0)

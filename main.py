import sys

import discord
from discord import app_commands
from discord.ext.commands import has_permissions

from client import fetch_config, Client
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
        if error_message:
            error = error_message
        if server_info:
            embed_message = discord.Embed(
                title=server_info.name,
                colour=discord.Colour.blurple(),
                description=f"Server Version: {server_info.version}",
            )
            format_embed(embed_message)
    except Exception as e:
        log.error(f"Unable to fetch/send game server info: {e}")
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
    error = config["generic_bot_error"]
    try:
        rcon_client = Client(config=config)
        players, error_message = rcon_client.online()
        if error_message:
            error = error_message
        player_count = len(players)
        embed_message = discord.Embed(
            title="Players Online",
            colour=discord.Colour.blurple(),
            description=f"Player(s) Online: {player_count}",
        )
        format_embed(embed_message)

        # TODO: Add a pagination system for when there are a lot of players online
        if player_count:
            buffer = []
            for key, value in players.items():
                buffer.append(f"[{value}]({STEAM_PROFILE_URL.format(steam_id=key)})")
            embed_message.add_field(name="Players", value="\n".join(buffer), inline=False)
    except Exception as e:
        log.error(f"Unable to fetch/send metadata of connected players: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(error)


@tree.command(
    name="save",
    description="Save the game server state",
)
@has_permissions(administrator=True)
async def save(interaction: discord.Interaction):
    embed_message = None
    error = config["generic_bot_error"]
    try:
        rcon_client = Client(config=config)
        response = rcon_client.save()

        embed_message = discord.Embed(
            title="Server Saving",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)
    except Exception as e:
        log.error(f"Unable to save game server state: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(error)

@tree.command(
    name="shutdown",
    description="Shutdown the server, with optional message and delay",
)
@has_permissions(administrator=True)
async def shutdown(interaction: discord.Interaction, seconds: int, message: str):
    embed_message = None
    error = config["generic_bot_error"]
    try:
        rcon_client = Client(config=config)
        response = rcon_client.shutdown(seconds, message)
        embed_message = discord.Embed(
            title="Server Shutdown",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)
    except Exception as e:
        log.error(f"Unable to shutdown game server: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(error)

# End of Slash Commands --------------------------------------------------------
def main(discord_bot_token):
    if not config:
        log.info("Shutting down PalCON...")
        logger.shutdown_logger()
        sys.exit(0)
    log.info("Configuration files loaded")

    log.info("Starting PalCON Discord Bot...")
    discord_client.run(discord_bot_token)


if __name__ == "__main__":
    main(config["discord_bot_token"])
    
    logger.shutdown_logger()
    sys.exit(0)

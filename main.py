import sys

import discord
from discord import app_commands
from discord.ext.commands import has_permissions

from client import fetch_config, Client
import logger


# Set-up logger & RCON client
log = logger.get_logger(__name__)
CONFIG = fetch_config()
if not CONFIG:
    log.info("Shutting down PalCON...")
    logger.shutdown_logger()
    sys.exit(0)
log.info("Configuration files loaded")
RCON_CLIENT = Client(CONFIG)

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
    embedded_message.set_footer(text=CONFIG["embed_footer"])
    embedded_message.set_thumbnail(url=CONFIG["embed_thumbnail"])


# Start of Slash Commands ------------------------------------------------------
@tree.command(
    name="info",
    description="Get server information",
)
async def info(interaction: discord.Interaction):
    embed_message = None
    try:
        server_info = await RCON_CLIENT.info()
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
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="online",
    description="Get information about all online players",
)
async def online(interaction: discord.Interaction):
    embed_message = None
    try:
        players, faulty = await RCON_CLIENT.online()

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

        if faulty:
            embed_message.add_field(
                name="Warning",
                value="One (or more) player's data could not be read, and were skipped.",
                inline=False
            )
    except Exception as e:
        log.error(f"Unable to fetch/send metadata of connected players: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="save",
    description="Save the game server state",
)
@has_permissions(administrator=True)
async def save(interaction: discord.Interaction):
    embed_message = None
    try:
        response = await RCON_CLIENT.save()

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
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="shutdown",
    description="Shutdown the server, with optional message and delay",
)
@has_permissions(administrator=True)
async def shutdown(interaction: discord.Interaction, seconds: int, message: str):
    embed_message = None
    try:
        # remove spaces
        formatted_message = message.replace(" ", "_")

        response = await RCON_CLIENT.shutdown(str(seconds), formatted_message)
        embed_message = discord.Embed(
            title="Server Shutdown",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)

        if len(message) > 50:
            embed_message.add_field(
                name="Warning",
                value="Messages longer than 50 characters will be truncated.",
                inline=False
            )
    except Exception as e:
        log.error(f"Unable to shutdown game server: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="announce",
    description="Make an announcement in-game (spaces replaced with underscores)",
)
@has_permissions(administrator=True)
async def announce(interaction: discord.Interaction, message: str):
    embed_message = None
    try:
        # remove spaces
        formatted_message = message.replace(" ", "_")

        response = await RCON_CLIENT.announce(formatted_message)

        embed_message = discord.Embed(
            title="Making In-game Announcement",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)

        if len(message) > 50:
            embed_message.add_field(
                name="Warning",
                value="Messages longer than 50 characters will be truncated.",
                inline=False
            )
    except Exception as e:
        log.error(f"Unable to make game announcement: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="kick",
    description="Kick a player from the game using Steam ID",
)
@has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, steam_id: str):
    embed_message = None
    try:
        player_ign = await RCON_CLIENT.get_ign_from_steam_id(steam_id)
        formatted_ign = f"[{player_ign}]({STEAM_PROFILE_URL.format(steam_id=steam_id)})" if player_ign else ""
        response = await RCON_CLIENT.kick(steam_id)

        embed_message = discord.Embed(
            title=f"Kicking player {formatted_ign}",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)
    except Exception as e:
        log.error(f"Unable to kick player: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="ban_player",
    description="Ban a player using Steam ID",
)
@has_permissions(administrator=True)
async def ban_player(interaction: discord.Interaction, steam_id: str):
    embed_message = None
    try:
        player_ign = await RCON_CLIENT.get_ign_from_steam_id(steam_id)
        formatted_ign = f"[{player_ign}]({STEAM_PROFILE_URL.format(steam_id=steam_id)})" if player_ign else ""
        response = await RCON_CLIENT.ban(steam_id)

        embed_message = discord.Embed(
            title=f"Banning player {formatted_ign}",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)
    except Exception as e:
        log.error(f"Unable to ban player: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(CONFIG["generic_bot_error"])


@tree.command(
    name="kill",
    description="Force-kill the server immediately",
)
@has_permissions(administrator=True)
async def kill(interaction: discord.Interaction):
    embed_message = None
    try:
        response = await RCON_CLIENT.force_stop()
        embed_message = discord.Embed(
            title="Forcing Server Termination",
            colour=discord.Colour.blurple(),
            description=response,
        )
        format_embed(embed_message)
    except Exception as e:
        log.error(f"Unable to forcibly terminate game server: {e}")
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(CONFIG["generic_bot_error"])


# End of Slash Commands --------------------------------------------------------
def main():
    log.info("Starting PalCON Discord Bot...")
    discord_client.run(CONFIG["discord_bot_token"])


if __name__ == "__main__":
    main()
    
    logger.shutdown_logger()
    sys.exit(0)

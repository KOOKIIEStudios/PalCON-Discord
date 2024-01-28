import sys
import discord

import logger
from client import fetch_config, Client
from discord import app_commands

GUILD_ID = 631249406775132180

config = fetch_config()
log = logger.get_logger(__name__)

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(*args, **kwargs, intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=GUILD_ID))
            self.synced = True
        log.info("Bot is online!")

discord_client = DiscordClient()
tree = app_commands.CommandTree(discord_client)

# Start of Slash Commands -------------------------------------------------------------------------------------------

@tree.command(
    name="info",
    description="Get server information",
    guilds=[discord.Object(id=GUILD_ID)]
)
async def info(interaction: discord.Interaction):
    try:
        rcon_client = Client()
        output = rcon_client.info()
    except Exception as e:
        log.error(f"Exception occurred while executing command: {e}")
        output = "Unable to process your request (server did not respond)"
    await interaction.response.send_message(output)

@tree.command(
    name="online",
    description="Get information about all online players",
    guilds=[discord.Object(id=GUILD_ID)]
)
async def online(interaction: discord.Interaction):
    try:
        rcon_client = Client()
        output = rcon_client.online()
    except Exception as e:
        log.error(f"Exception occurred while executing command: {e}")
        output = "Unable to process your request (server did not respond)"
    await interaction.response.send_message(output)

# End of Slash Commands ---------------------------------------------------------------------------------------------

def main(discord_bot_token):
    log.info("Starting PalCON Discord Bot...")
    discord_client.run(discord_bot_token)

if __name__ == "__main__":
    test_fetch_config = fetch_config()
    if not test_fetch_config:
        logger.shutdown_logger()
        sys.exit(0)

    main(test_fetch_config['discord_bot_token'])
    
    logger.shutdown_logger()
    sys.exit(0)

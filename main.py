import sys
import discord

import logger
from client import fetch_config, Client
from discord import app_commands

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

# Start of Slash Commands -------------------------------------------------------------------------------------------

@tree.command(
    name="info",
    description="Get server information",
)
async def info(interaction: discord.Interaction):
    try:
        rcon_client = Client()
        output = rcon_client.info()
        embed_message = discord.Embed(title=output, colour=discord.Colour.blurple(), description="Server Description Here")
        embed_message.set_footer(text="@PalCONBot")
        embed_message.set_thumbnail(url="https://media.discordapp.net/attachments/631249406775132182/1201307493163335680/relaxasarus.png?ex=65c957c9&is=65b6e2c9&hm=e0a820d7130239e6ef16b6bd5ec86bdc1976c63740aaccc842ba19c29f85ecf2&=&format=webp&quality=lossless")
    except Exception as e:
        log.error(f"Exception occurred while executing command: {e}")
        output = "Unable to process your request (server did not respond)"
    if embed_message:
        await interaction.response.send_message(embed=embed_message)
    else:
        await interaction.response.send_message(output)

@tree.command(
    name="online",
    description="Get information about all online players",
)
async def online(interaction: discord.Interaction):
    try:
        rcon_client = Client()
        output, players = rcon_client.online()
        embed_message = discord.Embed(title="Players Online", colour=discord.Colour.blurple(), description=f"Player(s) Online: {len(players)}")
        embed_message.set_thumbnail(url="https://media.discordapp.net/attachments/631249406775132182/1201307493163335680/relaxasarus.png?ex=65c957c9&is=65b6e2c9&hm=e0a820d7130239e6ef16b6bd5ec86bdc1976c63740aaccc842ba19c29f85ecf2&=&format=webp&quality=lossless")
        embed_message.set_footer(text="@PalCONBot")

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

# PalCON Discord
A Python-based Discord bot for PalWorld server administration via RCON .

This is an experimental project for a PalWorld remote console via Discord chat bot.
Control and monitor your Pal World Servers remotely using this Discord Bot.

See Gallery below to view some of the features the bot provides.

## Gallery

![Info](https://github.com/KOOKIIEStudios/PalCON-Discord/assets/58405975/a3a75e93-7b67-408b-8b53-93470dba9a0f)

![OnlineCommand](https://media.discordapp.net/attachments/1025357797937905746/1201312320371036170/image.png?ex=65c95c48&is=65b6e748&hm=1e36f1ec857df19f623663f5157f213f7340bb3e78033c8af263c78d7692607f&=&format=webp&quality=lossless)

![Save](https://github.com/KOOKIIEStudios/PalCON-Discord/assets/58405975/7d518b99-067a-4452-a5d9-4cd02d755b90)

![ShutdownSlashCommand](https://github.com/KOOKIIEStudios/PalCON-Discord/assets/58405975/efde4aec-a07d-48f1-80be-894548c5267c)

![Shutdown](https://github.com/KOOKIIEStudios/PalCON-Discord/assets/58405975/e1127f4d-46bf-40f3-bb07-9047dae4d50f)

## Tech Stack
This project **requires** Python 3.11+; refer to Discord's official documentation for
instructions on how to set up a Discord bot.

## Environment Installation
0. Download [Python](https://www.python.org/downloads/) and **SET IT TO PATH DURING INSTALLATION**.
1. Clone this repository
2. Create a file `config.toml` at the root of the project, using the provided [`config_example.toml`](https://github.com/KOOKIIEStudios/PalCON-Discord/blob/main/config_example.toml) as a guide
3. *(Bash-only)* Use `setup.sh` to set up your virtual environment **if you're on Linux**.
      - If you're on Windows, running the `start.bat` file will automatically set up your virtual environment!
4. Use `start.bat`/`start.sh` to run the Discord Bot!
    - Log files are saved to `/logs` and rotated at midnight.
    - Log files are automatically excluded from git

## Discord Bot Setup
1. Create your Discord Bot using the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click on New Application at the top right of the web page.
    - Insert a Name and click `Create` and click on your new Application.
  
    ![New Application](https://media.discordapp.net/attachments/631249406775132182/1201295694728798269/image.png?ex=65c94ccc&is=65b6d7cc&hm=c337d19900fd088f2551ca4aa1efa2195ee503b831f5d0007a5e3a794069cd80&=&format=webp&quality=lossless&width=1067&height=174)
3. Click on the `Bot` Section of the Discord Application:

    ![Bot](https://media.discordapp.net/attachments/631249406775132182/1201296343415652432/image.png?ex=65c94d67&is=65b6d867&hm=2e1a062af0f0b3a85b50279afdfb5c4b0ef84c62d1641c258013300706206a04&=&format=webp&quality=lossless&width=1067&height=333)
4. Copy your discord bot token and put it into the `config.toml` that you've created.
5. Ensure your discord bot has these settings appropriately marked.

    ![Discord Bot Settings](https://media.discordapp.net/attachments/631249406775132182/1201297358776975411/image.png?ex=65c94e59&is=65b6d959&hm=211219c172e981c06631b10fca34eedd1fb9c78b8f6293e39d79dba118cd3857&=&format=webp&quality=lossless&width=1023&height=557)
6. Invite the Discord Bot with the following scopes: bot & applications.commands
   
   ![Permissions](https://media.discordapp.net/attachments/631249406775132182/1201297573403701379/image.png?ex=65c94e8c&is=65b6d98c&hm=c6a248e6a2a91cc45f3a99c6f3959306363a7eb14751ae15a62794300718b663&=&format=webp&quality=lossless&width=1067&height=363)
> [!TIP]
Use a [Discord Permissions Calculator](https://discord.com/developers/applications/1201282683205062676/oauth2/url-generator) to make your life easier!

> [!IMPORTANT]
Do note that the slash commands may take up to an hour to propgate for ALL servers the bot is on.

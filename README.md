# PalCON Discord
A Python-based Discord bot for PalWorld server administration via RCON.

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
This project **requires** Python 3.11+. This is a pain point for Linux users, as Ubuntu Jammy (we have not checked other distros) currently only officially supports 3.10. We've included instructions for users who are on Ubuntu in the following section.

We initially wanted to use [Richard Neumann's RCON client implementation](https://pypi.org/project/rcon/), 
but since Palworld's RCON server doesn't follow specifications properly, said library wasn't working for Palworld. 
We have currently switched to [tama's implementation](https://github.com/ttk1/py-rcon), which is technically for Minecraft, but is working for us. One caveat (based on issue [#6](https://github.com/KOOKIIEStudios/PalCON-Discord/issues/6)) being that it makes assumptions about encoding, which causes packet read errors when players have non-latin characters in their IGN (not an issue for Minecraft which only allows latin characters).

## Environment Installation
1. *(Windows)* Download [Python](https://www.python.org/downloads/) and **SET IT TO PATH DURING INSTALLATION**.
   ![image](https://github.com/KOOKIIEStudios/PalCON-Discord/assets/58405975/abe48ef4-01bb-45d7-81ba-d9b6a38846e0)
   - Note: If you install using a package manager like Chocolatey, this will be done for you automatically
   - Instructions for Linux can be found in the following sub-section
2. Clone this repository
3. Create a file `config.toml` at the root of the project, using the provided [`config_example.toml`](https://github.com/KOOKIIEStudios/PalCON-Discord/blob/main/config_example.toml) as a guide
   - For Discord bot token, see the following section for instructions for setting up your own Discord bot
   - For IP address, use the public IP of your game server if the Discord bot is not on the same machine; otherwise `localhost` is fine
   - For port and password, see the RCON server set-up section below
4. *(UNIX-like)* Use `setup.sh` to set up your virtual environment
      - Note: Script files require permissions; e.g.: `chmod +x setup.sh start.sh`
      - If you're on Windows, running the `start.bat` file will automatically set up your virtual environment!
5. Use `start.bat`/`start.sh` to run the Discord Bot!
    - Log files are saved to `/logs` and rotated at midnight.
    - Log files are automatically excluded from git
5. The first time you run the bot, you will need to run the `!sync` command to sync the slash commands to Discord

### Installing Python 3.11 on Ubuntu Jammy
*Credits: Adapted from [an article Rehan Haider](https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux)*

This is only a temporary measure until Ubuntu officially adds support for Python 3.11+.

1. Update your system: `sudo apt update && sudo apt upgrade -y`
2. Add deadsnakes as third party repository: `sudo add-apt-repository ppa:deadsnakes/ppa`
3. Fetch package list: `sudo apt update`
4. Install Python 3.11 `sudo apt install python3.11`
5. Re-install the Python interface for APT
   - `sudo apt remove --purge python3-apt`
   - `sudo apt autoclean`
   - `sudo apt install python3-apt`
6. Manually install distutils: `sudo apt install python3.11-distutils`
7. Manually install pip
   - `cd` to a temporary location
   - Download the installation script: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` 
   - Run the installation script: `sudo python3.11 get-pip.py`
8. Manually install venv: `sudo apt install python3.11-venv`
9. `nano setup.sh` and `nano start.sh` to replace all instances of `python3` with `python3.11`

### Updating PalCON-Discord
We don't provide release versions, nor package the contents of this repository, 
so you can update to the latest version by simply performing `git pull`.

Note that [pull request #5](https://github.com/KOOKIIEStudios/PalCON-Discord/pull/5) has made command-syncing invocation-based, instead of occurring automatically on-ready. This means that when you wish to update PalCON, you'll need to call the `/sync` command as an administrator in Discord, after you pulled changes.

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
Do note that the slash commands may take up to an hour to propagate for ALL servers the bot is on.


## RCON Server Set-up
1. Open the Palworld configuration file using the appropriate path
   - The following are relative paths to Steam/SteamCMD's install directory: 
     - Windows: `steamapps/common/PalServer/Pal/Saved/Config/WindowsServer/PalWorldSettings.ini`
     - Linux: `steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini`
2. Scroll all the way to the right of the second line
3. Set the RCON port using the `RCONPort` variable
   - e.g. `RCONPort=255575`
4. Turn on RCON: `RCONEnabled=True`
5. Set the administrator password for toggling admin mode (this also doubles as the RCON password)
   - e.g. `AdminPassword="insertpasswordhere"`
6. Modify firewall rules for the RCON port
   - e.g. `sudo ufw allow 255575/tcp`
   - **MAKE SURE YOU'RE AWARE OF THE SECURITY RISKS OF DOING SO**
7. Port-forward the RCON port
   - Refer to your router's instructions for more details

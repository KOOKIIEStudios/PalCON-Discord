# PalCON Discord
A Python-based Discord bot for PalWorld server administration via RCON .

This is an experimental project for a PalWorld remote console via Discord chat bot.

## Tech Stack
This project requires Python 3.10+; refer to Discord's official documentation for
instructions on how to set up a Discord bot. 

## Usage
1. Clone this repository
2. Create a file `config.toml`, using the provided `config_example.toml` as a guide
3. *(Bash-only)* Use `setup.sh` to set up your virtual environment
4. Use `start.bat`/`start.sh` to run the program
    - Log files are saved to `/logs` and rotated at midnight.
    - Log files are automatically excluded from git
# Maple Bot

## Description

Maple Bot is a discord bot with customized slash commands. Its focus is on retrieving data and providing it for users on
discord where the bot is added.

## Setup
1. Make sure Python3.10+ is downloaded and installed
2. Git clone this project 
3. Create a new venv: `python -m venv /path/to/new/virtual/environment` preferably in the same folder as this project
4. Activate the venv if it's not running:
   - Windows - run `call venv/Scripts/activate` depending on where your venv is
   - Mac - run `source ./venv/bin/activate`
5. Now inside the `venv`, install the required libraries with ` pip install -r requirements.txt`
6. Configure `resources/env.py` with the appropriate credentials:
   - `discord_bot_token` 
   - `discord_bot_guild`
   - `discord_guild_id`
7. Test by running `python src/maple_bot.py`

## Slash Commands
### Maple Ranking Commands
The commands in this section are for retrieving player data based on several parameters

### Other Commands
Additional Commands to be added

## Packages
- [`discord-py-interactions`](https://pypi.org/project/discord-py-interactions/) - A highly extensible, easy to use, and feature complete framework for Discord.
- [`requests`](https://pypi.org/project/requests/) -  send HTTP/1.1 requests
- [`selenium`](https://pypi.org/project/selenium/) - Python language bindings for Selenium WebDriver
- [`bs4`](https://pypi.org/project/beautifulsoup4/) - Package to handle XPath and Html pathing

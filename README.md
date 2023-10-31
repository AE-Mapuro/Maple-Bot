# Maple Bot (Grendel)

## Description

Grendel is a discord bot. 

It is meant to provide information about Maplestory, and may typically be invoked using various slash commands. As a proof of concept, it will only fetch ranking information directly from [Nexon](maplestory.nexon.net), for now. In the future, more functionality will be added, such as the ability to request specific information about game items, NPCs, and quests. 

## Requirements
- Python version 3.10+ - required for the `discord-py-interactions` package  
- [`discord-py-interactions`](https://pypi.org/project/discord-py-interactions/) - A highly extensible, easy to use, and feature complete framework for Discord.
- [`selenium`](https://pypi.org/project/selenium/) - Python language bindings for the Selenium WebDriver
- [`bs4`](https://pypi.org/project/beautifulsoup4/) - Package to handle XPath and Html pathing

## Setup
Python3.10+ is required for the bot to run. 
Run `python --version` to verify this. 
[Download and install](https://www.python.org/downloads/) it if the python version is insufficient. 
1. Clone this repository  
   `git clone https://github.com/AE-Mapuro/Maple-Bot.git`
2. Navigate to the folder  
   `cd Maple-Bot`
3. Instantiate a python virtual environment<sup>[1]</sup>  
   `python -m venv pyenv`
4. Activate the virtual environment<sup>[2]</sup>  
   - Windows - `.\pyenv\Scripts\activate`
   - Linux/Mac - `source ./pyenv/bin/activate`
5. Install the required python packages
   `pip install -r requirements.txt`
6. Create an `env.py` file to contain the bot credentials.
   Do this by copying the existing barebones `env_template.py` file.  
   `cp resources/env_template.py resources/env.py`
7. Configure `resources/env.py` with the appropriate credentials:
   - `discord_bot_token` 
   - `discord_bot_guild`
   - `discord_guild_id`
8. Start up the bot
    `python -m src.bot.py`

---

<sup>[1]</sup> Instead of `pyenv`, you can specify a literal path to where you want the virtual environment folder to reside (e.g. `~/path/to/env_fol`)  
<sup>[2]</sup> Replace the `pyenv` path with the actual path to your virtual environment folder, if necessary  

## Slash Commands
### Maple Ranking Commands
The commands in this section are for retrieving player data based on several parameters

### Other Commands
Additional Commands to be added

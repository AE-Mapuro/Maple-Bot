from interactions import *
from resources import env

intents = Intents.DEFAULT | Intents.MESSAGE_CONTENT | Intents.PRIVILEGED | Intents.GUILDS
# intents = Intents.MESSAGE_CONTENT | Intents.PRIVILEGED | Intents.GUILDS | Intents.PRIVILEGED

client = Client(intents=intents, description="Maple Bot")


# First to indicate successful login
@listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")


# Load Extensions
# We may want to use iteration on a folder in the future
# https://interactions-py.github.io/interactions.py/Guides/20%20Extensions/#advanced-usage
client.load_extension("src.exts.shenanigans.shenanigans")
client.load_extension("src.exts.shenanigans.ask")
client.load_extension("src.exts.shenanigans.react")
client.load_extension("src.exts.utilities.utility")
client.load_extension("src.exts.utilities.poll")

# Start the bot
client.start(env.discord_bot_token)



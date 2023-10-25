import interactions
from resources import env

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
client = interactions.Client(intents=intents, description="Maple Bot")


# First to indicate successful login
@interactions.listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")


# Start the bot
client.start(env.discord_bot_token)
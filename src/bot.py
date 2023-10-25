import interactions
from resources import env
import random

intents = interactions.Intents.DEFAULT | interactions.Intents.MESSAGE_CONTENT
client = interactions.Client(intents=intents, description="Maple Bot")


# First to indicate successful login
@interactions.listen()
async def on_ready():
    # We can use the client "me" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.user.username}.")


@interactions.slash_command(name='ask', description='Ask Grendel Bot a question',
                            scopes=env.discord_guild_id)
@interactions.slash_option(
    name='question',
    description="Question asked by the user",
    required=True,
    opt_type=interactions.OptionType.STRING
)
async def askGrendel(ctx: interactions.SlashContext, question: interactions.OptionType.STRING):
    responses = ['', 'No', 'Whyyyy', 'Nani', 'Jes', 'Nani Kore', 'Watashi wa Kotowaru', 'Plz', 'Plz No', 'No Violins Plox', 'This is too difficult to answer']
    expressions = ['(ㆆ _ ㆆ)', '⊂(◉‿◉)つ', '•`_´•', 'ʕっ•ᴥ•ʔっ', '(•_•) ( •_•)>⌐■-■ (⌐■_■)', '(｡◕‿‿◕｡)', '(︶︹︶)', '┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻', '(ง •̀_•́)ง', '(ノಠ益ಠ)ノ彡┻━┻', '¯\_(ツ)_/¯']

    print(f'Command Message - ID: {ctx.message_id} -> {ctx.message}')
    await ctx.send(f"{random.choice(responses)} {random.choice(expressions)}")

# Start the bot
client.start(env.discord_bot_token)
import interactions
from resources import env
import random

from interactions import Snowflake_Type

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
@interactions.slash_option(
    name='number_of_question_marks',
    description="Severity of question asked",
    required=False,
    opt_type=interactions.OptionType.INTEGER
)
async def askGrendel(ctx: interactions.SlashContext, question: interactions.OptionType.STRING, number_of_question_marks: interactions.OptionType.INTEGER = 1):
    responses = ['', 'No', 'Whyyyy', 'Nani', 'Jes', 'Nani Kore', 'Watashi wa Kotowaru', 'Plz', 'Plz No', 'No Violins Plox', 'This is too difficult to answer']
    expressions = ['(ㆆ _ ㆆ)', '⊂(◉‿◉)つ', '•`_´•', 'ʕっ•ᴥ•ʔっ', '(•_•) ( •_•)>⌐■-■ (⌐■_■)', '(｡◕‿‿◕｡)', '(︶︹︶)', '┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻', '(ง •̀_•́)ง', '(ノಠ益ಠ)ノ彡┻━┻', R'¯\_(ツ)_/¯']

    print(f'Command Message - ID: {ctx.message_id} -> {ctx.message}')
    # await ctx.send(f"{random.choice(responses)} {random.choice(expressions)}")
    await ctx.send(f"{question}{'?' * number_of_question_marks}")
    await ctx.send(f"{random.choice(responses)} {random.choice(expressions)}")

# Start the bot
client.start(env.discord_bot_token)
from interactions import *
from interactions.api.events import Component
import random

class RockPaperScissors(Extension):
    choices = ['rock', 'paper', 'scissor']
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSOR = 'scissor'

    def __init__(self, bot):
        self.games = {}

    def build_game_embed(self) -> Embed:
        embed = Embed(title="Let's Play Rock Paper Scissors!",
                      description='Rock, Paper, or Scissors?',
                      color=Color.from_rgb(255, 102, 255),
                      timestamp=Timestamp.now())
        return embed

    def build_buttons(self) -> list[Button]:
        return [Button(
            style=ButtonStyle.GREEN,
            emoji='🪨',
            custom_id=f'rock'
        ), Button(
            style=ButtonStyle.GREEN,
            emoji='📃',
            custom_id=f'paper',
        ), Button(
            style=ButtonStyle.GREEN,
            emoji='✂',
            custom_id=f'scissor',
        )]

    def add_new_player(self, user_id: str, user_name: str):
        self.games[user_id] = {"username": user_name,
                               "net_score": 0,
                               "user_score": 0,
                               "bot_score": 0,
                               "tie": 0}

    @listen(Component)
    async def my_callback(self, event: Component):
        ctx = event.ctx
        user_id = str(ctx.user.id)
        user_choice = ctx.custom_id
        user_name = ctx.user.display_name

        if user_id not in self.games:
            self.add_new_player(user_id, user_name)

        user_score = self.games.get(user_id, {}).get("user_score", 0)
        bot_score = self.games.get(user_id, {}).get("bot_score", 0)
        tie = self.games.get(user_id, {}).get("tie", 0)

        bot_choice = random.choice(self.choices)

        if bot_choice == user_choice:
            tie += 1
            self.games.get(user_id, {})["tie"] = tie
            await ctx.send(f"Looks like we both chose {bot_choice}. Its a tie!")
        elif (bot_choice == self.ROCK and user_choice == self.PAPER) or (
                bot_choice == self.PAPER and user_choice == self.SCISSOR) or (
                bot_choice == self.SCISSOR and user_choice == self.ROCK):
            user_score += 1
            self.games.get(user_id, {})["user_score"] = user_score
            await ctx.send(f"I chose {bot_choice}, you chose {user_choice}. You won!")
        else:
            bot_score += 1
            self.games.get(user_id, {})["bot_score"] = bot_score
            await ctx.send(f"I chose {bot_choice}, you chose {user_choice}. You lost!")

        self.games.get(user_id, {})["net_score"] = user_score - bot_score

def setup(bot):
    RockPaperScissors(bot)
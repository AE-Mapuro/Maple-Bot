from interactions import *

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

def setup(bot):
    RockPaperScissors(bot)
from interactions import *

class RockPaperScissors(Extension):
    choices = ['rock', 'paper', 'scissor']
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSOR = 'scissor'

    def __init__(self, bot):
        self.games = {}


def setup(bot):
    RockPaperScissors(bot)
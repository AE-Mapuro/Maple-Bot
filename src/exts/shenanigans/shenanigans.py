import random
from resources import env
from interactions import Extension, slash_command, SlashContext


# Extensions need to inherit from the Extensions class and loaded into the main bot class
class ShenaniganCommands(Extension):

    @slash_command(name='shenanigans',
                   description='Random cmds for no reason',
                   sub_cmd_name='info',
                   sub_cmd_description='List of cmds under shenanigans',
                   scopes=env.discord_guild_ids)
    async def shenanigans(self, ctx: SlashContext):
        information = '''
            `rng` - Randomly generated number between 0 - 100
            `ask` - And ye shall receive
        '''
        await ctx.send(information)

    @shenanigans.subcommand(sub_cmd_name='rng', sub_cmd_description=f'RNG')
    async def askCommand(self, ctx: SlashContext):
        await ctx.send(str(int(random.random() * 100)))


def setup(bot):
    ShenaniganCommands(bot)

import random
from resources import env
from interactions import *


# Extensions need to inherit from the Extensions class and loaded into the main bot class
def get_cmd_information():
    return \
        '''
        ### `rng` - Randomly generated number between 0 - 100
### `ask` - And ye shall receive.
- `question` - Your question to wise Grendel
- `severity` - How severe is your question??
### `toggle` - Toggle auto msg reacts for the user
- `user` - optional argument to select specific user. Default is yourself 
    '''


class ShenaniganCommands(Extension):

    @slash_command(name='shenanigans',
                   description='Random cmds for no reason',
                   sub_cmd_name='info',
                   sub_cmd_description='List of cmds under shenanigans',
                   scopes=env.discord_guild_ids)
    async def shenanigans(self, ctx: SlashContext):
        information = get_cmd_information()

        embed = Embed(title='<:sophia_wat:886857371689844737> Shenanigan Commands Info',
                      description=information,
                      color=Color.from_rgb(98, 242, 175))
        await ctx.send(embeds=embed)

    @shenanigans.subcommand(sub_cmd_name='rng', sub_cmd_description=f'RNG')
    async def askCommand(self, ctx: SlashContext):
        await ctx.send(str(int(random.random() * 100)))


def setup(bot):
    ShenaniganCommands(bot)

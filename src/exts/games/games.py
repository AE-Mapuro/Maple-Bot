from interactions import *


def get_cmd_information():
    return \
        '''### `rps` - Start a Rock Paper Scissors Game 
/util rps'''


class Games(Extension):
    @slash_command(name='games',
                   description='Subcommand for different games maple bot can do',
                   sub_cmd_name='info',
                   sub_cmd_description='Information on available games')
    async def info(self, ctx: SlashContext):
        information = get_cmd_information()

        embed = Embed(title='<:bugcat_hate:886858534032138272> **Games Commands Info** '
                            '<:bugcat_hate:886858534032138272>',
                      description=information,
                      color=Color.from_rgb(98, 242, 175))
        await ctx.send(embeds=embed)


def setup(bot):
    Games(bot)

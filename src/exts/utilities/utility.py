from interactions import *
import resources.env as env


def get_cmd_information():
    return \
        '''### `poll` - Create a poll 
- `question` - Your question to everybody
- `choices` - Choices separated by g"|" and with "~" for each <emoji>~<choice> if a custom emoji is desired such as 🍔~A|🍝~B|C. Limit 10
/util poll question| What item? choices| 🔮~Globe|🎃~Pumpkin|Cookie'''


class Utility(Extension):

    @slash_command(name='util',
                   description='Utility Commands for something useful perhaps',
                   sub_cmd_name='info',
                   sub_cmd_description='Info on available utility commands',
                   scopes=env.discord_guild_ids)
    async def info(self, ctx: SlashContext):
        information = get_cmd_information()

        embed = Embed(title='<a:bugcat_keyboard_smash:1201274359705239635> **Utility Commands Info** '
                            '<a:bugcat_keyboard_smash:1201274359705239635>',
                      description=information,
                      color=Color.from_rgb(98, 242, 175))
        await ctx.send(embeds=embed)


def setup(bot):
    Utility(bot)

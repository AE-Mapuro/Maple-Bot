from interactions import *
from interactions.api.events import *
from resources import env
from src.exts.shenanigans.shenanigans import ShenaniganCommands as SC


class React(Extension):
    def __init__(self, bot):
        self.react_toggle_on = False
        self.users = {}

    @listen(Startup)
    async def react_startup(self):
        guild = await self.bot.fetch_guild(env.discord_guild_ids[0])
        for member in guild.members:
            self.users[member.user.display_name] = False

    @listen(MessageCreate)
    async def handle_message(self, event: MessageCreate):
        if event.message.author.display_name in self.users and self.users[event.message.author.display_name]:
            await event.message.add_reaction(emoji='<:bugcat_cry:886858534136987678>')

    @SC.shenanigans.subcommand(sub_cmd_name='cry',
                               sub_cmd_description='Toggle the auto reaction on or off')
    @slash_option(name='user',
                  description='User to be toggled On or Off',
                  opt_type=OptionType.USER,
                  required=False)
    async def toggle_react(self, ctx: SlashContext, user: User = None):
        display_name = ctx.author.display_name if user is None else user.display_name

        # If the member to toggle doesn't exist, add them in
        if display_name not in self.users:
            self.users[display_name] = False

        # Toggle the saved flag
        self.users[display_name] = True if not self.users[display_name] else False
        await ctx.send(f'Reaction Toggle is now set to: {self.users[display_name]} for {display_name}')


def setup(bot):
    React(bot)

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
            self.users[member.user.username] = False


    @listen(MessageCreate)
    async def handle_message(self, event: MessageCreate):
        if event.message.author.username in self.users and self.users[event.message.author.username]:
            await event.message.add_reaction(emoji='<:bugcat_cry:886858534136987678>')

    @SC.shenanigans.subcommand(sub_cmd_name='toggle',
                               sub_cmd_description='Toggle the auto reaction on or off')
    @slash_option(name='user',
                  description='User to be toggled On or Off',
                  opt_type=OptionType.USER,
                  required=False)
    async def toggle_react(self, ctx: SlashContext, user: User = None):
        username = ctx.author.username if user is None else user.username

        # If the member to toggle doesn't exist, add them in
        if username not in self.users:
            self.users[username] = False

        # Toggle the saved flag
        self.users[username] = True if not self.users[username] else False
        await ctx.send(f'Reaction Toggle is now set to: {self.users[username]} for {username}')


def setup(bot):
    React(bot)

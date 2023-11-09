import random
from resources import env
from interactions import Extension, slash_command, SlashContext


# Extensions need to inherit from the Extensions class and loaded into the main bot class
class ShenaniganCommands(Extension):
    @slash_command(name='rng', description=f'RNG',
                   scopes=env.discord_guild_id)
    async def askCommand(self, ctx: SlashContext):
        await ctx.send(str(int(random.random() * 100)))

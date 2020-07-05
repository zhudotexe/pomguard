from discord.ext import commands


class Lookups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Lookups(bot))

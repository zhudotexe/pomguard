import random

import discord
from discord.ext import commands

from utils import fashionreport


class Lookups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fashionreport', aliases=['fr'])
    async def fashion(self, ctx):
        embed = discord.Embed()
        embed.colour = random.randint(0, 0xffffff)
        latest = await fashionreport.get_latest(self.bot)
        embed.description = latest.text
        embed.set_image(url=latest.media[0].media_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Lookups(bot))

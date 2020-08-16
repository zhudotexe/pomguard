import os

import twitter
from discord.ext import commands
from discord.ext.commands import Bot

# auth
TOKEN = os.environ.get("TOKEN")
TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
TWITTER_TOKEN_KEY = os.environ.get("TWITTER_TOKEN_KEY")
TWITTER_TOKEN_SECRET = os.environ.get("TWITTER_TOKEN_SECRET")

# config
PREFIX = "!"
COGS = ("cogs.timers", "cogs.lookups", "cogs.tempchannels")


class Pomguard(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.twitter = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                                   consumer_secret=TWITTER_CONSUMER_SECRET,
                                   access_token_key=TWITTER_TOKEN_KEY,
                                   access_token_secret=TWITTER_TOKEN_SECRET)


bot = Pomguard(PREFIX)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    await ctx.send(str(error))


for cog in COGS:
    bot.load_extension(cog)

if __name__ == '__main__':
    bot.run(TOKEN)

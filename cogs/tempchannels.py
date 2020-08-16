import random
import typing

import discord
from discord.ext import commands

import constants


class TempChannelInfo:
    def __init__(self, category: discord.CategoryChannel, text_channel: discord.TextChannel,
                 voice_channel: discord.VoiceChannel, creator: discord.Member, invite: discord.Invite):
        self.category = category
        self.text_channel = text_channel
        self.voice_channel = voice_channel
        self.creator = creator
        self.invite = invite


class TempChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}  # int (textchannel id) -> TempChannelInfo
        self.all_invites = []
        bot.loop.create_task(self.on_load())

    async def on_load(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    @commands.command()
    @commands.has_role(constants.KUPO_ROLE_ID)
    async def tempchannel(self, ctx, max_invitees: typing.Optional[int] = None, *, channel_name=None):
        """
        Creates a temporary channel (for use with non-FC raiders, etc.)

        By default, the invite to this new channel will last for 24 hours and allow unlimited people to join, with
        temporary membership.

        - max_invitees: The maximum number of people the invite is allowed to add.
        - channel_name: The name for the tempchannel.

        When done with the channel, run `!close` to delete the channel.
        """
        # fc members get one tempchannel
        if ctx.author in [ch.creator for ch in self.temp_channels.values()]:
            return await ctx.send("You already have a tempchannel open. Close it with `!close` in the corresponding "
                                  "text channel first, kupo!")

        channel_name = channel_name or f"{random.choice(constants.TEMPCHANNEL_NAMES)} Temp"
        if max_invitees is None:
            max_invitees = 0

        async with ctx.typing():
            category = await ctx.guild.create_category(channel_name, reason=f"Tempchannel created by {ctx.author}")
            voice_channel = await category.create_voice_channel(
                f"{channel_name} Voice", user_limit=max_invitees or None)
            text_channel = await category.create_text_channel(channel_name)
            invite = await text_channel.create_invite(
                max_age=constants.SECONDS_ONE_DAY, max_uses=max_invitees, temporary=True)
            self.temp_channels[text_channel.id] = TempChannelInfo(
                category, text_channel, voice_channel, ctx.author, invite)
            welcome = await text_channel.send(
                f"Welcome to *{channel_name}*, kupo! This is a temporary channel created by a FC member for one or "
                f"more instances.\n\n"
                f"**For FC Members**: Remember to run `!close` when you're done with the channel! Here's a snippet to "
                f"paste into chat: ```\n"
                f"/p Hello, kupo! We've set up a temporary Discord channel to talk in for this instance if you'd like "
                f"to join: {invite.url}"
                f"```\n\n"
                f"**For Visitors**: Feel free to use channels in this category to chat and coordinate! "
                f"You will automatically be removed from this server the next time you log off, so let a FC member "
                f"know if you want to stay!"
            )
            await welcome.pin()
        await ctx.send(f"Created {text_channel.mention}, kupo!")

    @commands.command()
    @commands.has_role(constants.KUPO_ROLE_ID)
    async def close(self, ctx):
        """Closes a temporary channel."""
        if ctx.channel.id not in self.temp_channels:
            return await ctx.send("This channel is not a tempchannel, and cannot be deleted, kupo!")

        tempchannel_info = self.temp_channels[ctx.channel.id]

        try:
            await tempchannel_info.voice_channel.delete(reason=f"Tempchannel closed by {ctx.author}")
            await tempchannel_info.text_channel.delete(reason=f"Tempchannel closed by {ctx.author}")
            try:
                await tempchannel_info.invite.delete(reason=f"Tempchannel closed by {ctx.author}")
            except discord.NotFound:
                pass
            await tempchannel_info.category.delete(reason=f"Tempchannel closed by {ctx.author}")
        except discord.Forbidden:
            return await ctx.send("I do not have permission to delete this channel, kupo!")
        del self.temp_channels[ctx.channel.id]


def setup(bot):
    bot.add_cog(TempChannels(bot))

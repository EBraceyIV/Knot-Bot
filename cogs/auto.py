import discord
from discord.ext import commands


# This cog is dedicated to conducting automatic actions
class Auto(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        return


# Add the cog
def setup(bot):
    bot.add_cog(Auto(bot))
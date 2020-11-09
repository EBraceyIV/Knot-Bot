from discord.ext import commands
import random

autoReactEmoji = ["🎉", "👍", "✨", "💖", "🤩", "🧵", "😍", "❤"]


# This cog is dedicated to conducting automatic actions
class Auto(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global autoReactEmoji

        if message.attachments is not None:
            for attachment in message.attachments:
                if attachment.filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    for reaction in random.choices(autoReactEmoji, k=2):
                        await message.add_reaction(reaction)
                else:
                    print("pong")


# Add the cog
def setup(bot):
    bot.add_cog(Auto(bot))

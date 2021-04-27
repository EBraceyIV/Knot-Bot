#! python 3
import discord
from discord.ext import commands
import os
import TOKEN

# Bot setup
TOKEN = TOKEN.token()

bot = commands.Bot(command_prefix=["kb:", "Kb:", "kB:", "KB:"],
                   case_insensitive=True)


@bot.event
async def on_ready():
    # Console confirmation that the bot is now active
    print("KnotBot has logged in as {0}.".format(bot.user.name))
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f'cogs.{cog[:-3]}')
            except Exception as e:
                print("Couldn't load cog \"{0}\"".format(cog))
                print("Error: {0}".format(e))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with string."))


# # ERROR HANDLING
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I don't know that command. Check again or try another one.")


if __name__ == "__main__":
    bot.run(TOKEN)

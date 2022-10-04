# KNOT BOT
# Knot Bot is designed to integrate BraceletBook.com information at a glance in Discord. This bot is not affiliated in
# any official capacity with BraceletBook.com or its owner.
# Visit my repo for more information
# ----------------------------------------------------------------------------------------------------------------------
import discord
from discord.ext import commands
import os
import asyncio
import TOKEN

# TODO: Work on some kind of recommended products system and maybe user reviews
# TODO: Multi-server compatibility

# Bot setup
TOKEN = TOKEN.token()

bot = commands.Bot(command_prefix=["kb:", "Kb:", "kB:", "KB:"],
                   case_insensitive=True,
                   intents=discord.Intents.all())


# LOAD COGS
@bot.event
async def on_ready():
    # Console confirmation that the bot is now active
    print("KnotBot has logged in as {0}.".format(bot.user.name))
    # Load the cogs in the "cogs" directory
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{cog[:-3]}")
            except Exception as e:
                print("Couldn't load cog \"{0}\"".format(cog))
                print("Error: {0}".format(e))
    # Set the Discord presence of the bot on load
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with string."))


# ERROR HANDLING
@bot.event
async def on_command_error(ctx, error):
    # Inform a user if they've input a command that does not exist
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I don't know that command. Check again or try another one.")


async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())

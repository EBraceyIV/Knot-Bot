import discord
import shelve
import asyncio
from discord.ext import commands
from cogs.html import get_html
from mcstatus import MinecraftServer

# Load all of the stored usernames
usernames = shelve.open('BB_usernames')

# mcstatus init
server = MinecraftServer.lookup("192.99.4.195:25577")  # my minecraft server


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

# Commands

    # Provides current player count and latency to the Minecraft server
    @commands.command(name="blocks", help='Minecraft Server Info')
    async def blocks(self, ctx):
        # Get all of the server information
        status = server.status()

        # Build the embed message using the server query
        embed = discord.Embed(title='The Official Unofficial Bracelet Enthusiast Minecraft Server',
                              color=0xdd3333,
                              description='Come play with some blocks at {0}:{1}'
                              .format(server.host, server.port))
        embed.add_field(name='Players Online:', value=status.players.online)
        embed.add_field(name='Latency:', value=str(status.latency) + ' ms')
        embed.add_field(name='Game Version:', value=status.version.name)
        embed.set_footer(text='This server is hosted out of Houston, TX by Villagerhost.')
        await ctx.send(embed=embed)

    # bb:user <username>, store BB usernames for use
    @commands.command(name="user", help="Tell KnotBot your BraceletBook username.",
                      description="KnotBot can remember your BraceletBook username and apply automatically to any "
                                  "duplicate pattern reports you make.")
    async def user(self, ctx, username: str):
        # Store the provided username according the Discord name with #XXXX discriminator
        usernames[str(ctx.message.author)] = username
        # Send confirmation to channel
        await ctx.send("Thank you, " + str(ctx.message.author.display_name) +
                       "! I'll remember your BraceletBook username as " + username + " from now on.")

    # bb:dupe <original_id> <dupe_id>, file a "report" for duplicate patterns on BB
    @commands.command(name='dupe', help='Report a duplicate pattern on BraceletBook.')
    async def dupe(self, ctx, original_id: int, dupe_id: int):
        if ctx.channel.id != 741288985988694127:
            await ctx.reply("Please report duplicates in our dedicated channel!")
            return

        # Check username reply is from the right user
        def check(message):
            if ctx.message.author == message.author:
                return message

        # Know which user is creating the report
        report_creator = ctx.message.author.display_name

        # Verify that the patterns being reported exist so that they can be hyperlinked
        valid_id_original, pattern_info, style, url_original = get_html(original_id)
        valid_id_dupe, pattern_info, style, url_dupe = get_html(dupe_id)

        if not valid_id_original or not valid_id_dupe:
            # If either pattern doesn't exist, send a notice
            await ctx.send("Hm, seems like one of those patterns doesn't exist. Please double check and try again.")

        else:
            # Prompt for BB username if not already logged for user
            if str(ctx.message.author) not in usernames:
                await ctx.send("It seems like I don't know your BraceletBook username. "
                               "Send a message with just your BB username in it so I can finish your report, thanks!")
                try:
                    # For some reason I can't just get the message content directly, so I take the message then pluck it
                    bb_user = await self.bot.wait_for('message', timeout=60.0, check=check)
                    bb_user = bb_user.content
                except asyncio.TimeoutError:
                    await ctx.send("Oops, that took a little while. "
                                   "Please use `bb:user` and try your making your report again.")
                    return

                else:
                    # Store the username, send a confirmation and the requested report
                    usernames[str(ctx.message.author)] = bb_user
                    await ctx.send("Thank you, " + str(ctx.message.author.display_name) +
                                   "! I'll remember your BraceletBook username as " + bb_user + " from now on.")
                    await ctx.send("Here's your report: ")

            else:
                bb_user = usernames[str(ctx.message.author)]
            # Build and send the embed message
            embed = discord.Embed(title="Duplicate Pattern Report",
                                  description="This duplicate pattern report was made by " + report_creator + ", or " +
                                              bb_user + " on BraceletBook.",
                                  color=0xf7633f)
            embed.set_author(name=report_creator + " (" + bb_user + ")")
            embed.set_thumbnail(url='https://static.braceletbookcdn.com/images/logo_header.png')
            embed.add_field(name="Original Pattern",
                            value="[ID #" + str(original_id) + "](" + url_original + ")", inline=True)
            embed.add_field(name="Duplicate Pattern",
                            value="[ID #" + str(dupe_id) + "](" + url_dupe + ")", inline=True)
            embed.set_footer(text="This message does not indicate an actual report has been made to BB staff. "
                                  "This is for aggregation purposes and reference only. "
                                  "Thank you for your contribution.")
            await ctx.send(embed=embed)

# Error Handling
    @dupe.error
    async def user_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please try again and include your BraceletBook username.")

    @dupe.error
    async def dupe_arg_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Looks like you entered some info wrong, double check and try again.')

    @dupe.error
    async def dupe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Looks like you forgot something, double check and try again.')


# Add the cog
def setup(bot):
    bot.add_cog(Utility(bot))

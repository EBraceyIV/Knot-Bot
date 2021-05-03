import discord
from discord.ext import commands
import bs4
from cogs.html import *
import random


# This gets reused often so it's a function
def embed_init(bracelet_id, style, crafter, variations, url):
    description = style + crafter[0].getText() + "." \
                  if not variations else style + crafter[0].getText() + ".\n" + "Variations: " + variations
    embed = discord.Embed(title="Pattern #" + bracelet_id,
                          color=0xf7633f,
                          description=description,
                          url=url)
    embed.set_footer(text="For any questions/comments/concerns regarding this bot please contact the owner, "
                          "Kiwi Shark. He'll take a look when he gets the chance and appreciates the feedback.")
    return embed


def embed_extras(embed, crafter, crafter_url, crafter_icon):
    embed.set_author(name=crafter[0].getText(),
                     url=crafter_url[0].get("href"), icon_url=crafter_icon[0].get("src"))
    embed.set_thumbnail(url="https://static.braceletbookcdn.com/images/logo_header.png")
    return embed


class Bracelets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Display information about a pattern given its #ID
    @commands.command(name="id",
                      help="Provide a pattern ID from BB and get some info in the design!")
    async def id(self, ctx, bracelet_id):
        #  ID taken in as a string in case the user adds "#" to the start of the ID, as is sometimes common
        if bracelet_id[0] == "#":
            bracelet_id = bracelet_id[1:]

        try:
            int(bracelet_id)
        except ValueError:
            await ctx.reply("Looks like you entered the ID wrong, double check and try again.", mention_author=False)
            return

        valid_id, pattern_info, style, url = get_html(bracelet_id)

        if valid_id:
            # Gather all of the parts of the embed message
            braceletSoup = bs4.BeautifulSoup(pattern_info.text, "html.parser")
            crafter, crafter_icon, crafter_url = crafter_info(braceletSoup)
            dims, strings, colors, variations = pattern_data(braceletSoup)
            variations = "0" if variations == [] else variations[0].getText()
            preview = braceletSoup.select(".preview_svg img")
            pattern = braceletSoup.select(".pattern_image img")

            # Build the embed message
            embed = embed_init(bracelet_id, style, crafter, variations, url)
            embed.set_author(name=crafter[0].getText(),
                             url=crafter_url[0].get("href"), icon_url=crafter_icon[0].get("src"))
            embed.set_thumbnail(url=preview[0].get("src"))
            embed.add_field(name="Dimensions", value=dims[0].getText())
            embed.add_field(name="Strings", value=strings[0].getText())
            embed.add_field(name="Colors", value=colors[0].getText())
            embed.set_image(url=pattern[0].get("src"))

            await ctx.send(embed=embed)
        else:
            await ctx.reply("I couldn't find #" + bracelet_id + ", sorry about that.", mention_author=False)

    # Preview a finished bracelet
    @commands.command(name="pre",
                      help="Provide a pattern ID from BB and get a preview of a finished bracelet.")
    async def pre(self, ctx, bracelet_id: int):
        bracelet_id = str(bracelet_id)
        valid_id, pattern_info, style, url = get_html(bracelet_id)
        if valid_id:
            # Gather all of the parts of the embed message
            braceletSoup = bs4.BeautifulSoup(pattern_info.text, "html.parser")
            crafter, crafter_icon, crafter_url = crafter_info(braceletSoup)
            preview = braceletSoup.select(".preview_svg img")

            # Build the embed message
            embed = embed_init(bracelet_id, style, crafter, None, url)
            embed = embed_extras(embed, crafter,  crafter_url, crafter_icon)
            embed.set_image(url=preview[0].get("src"))

            await ctx.send(embed=embed)
        else:
            await ctx.reply("I couldn't find #" + bracelet_id + ", sorry about that.", mention_author=False)

    @commands.command(name="pic",
                      help="See a picture of a completed bracelet for a certain pattern!")
    async def pic(self, ctx, bracelet_id: int):
        bracelet_id = str(bracelet_id)
        valid_id, pattern_info, style, url = get_html(bracelet_id)
        if valid_id:
            # Gather all of the parts of the embed message
            braceletSoup = bs4.BeautifulSoup(pattern_info.text, "html.parser")
            crafter, crafter_icon, crafter_url = crafter_info(braceletSoup)
            pictures = braceletSoup.select(".photos_item > a")

            if not pictures:
                await ctx.reply("I couldn't find any pictures for #" + bracelet_id + ", sorry about that.",
                                mention_author=False)
            pic_num = random.randint(0, len(pictures)-1)
            picture = braceletSoup.select(".photos_item > a")[pic_num]
            pic_crafter = braceletSoup.select(".photos_item > .info > .added_by")[pic_num]

            # Build the embed message
            embed = embed_init(bracelet_id, style, crafter, None, url)
            embed = embed_extras(embed, crafter,  crafter_url, crafter_icon)

            embed.description = "This photo of #" + bracelet_id + " was uploaded " + pic_crafter.getText() + ". \n" + \
                                "It's one of " + str(len(pictures)) + " uploaded."
            embed.set_image(url=picture.get("href"))
            await ctx.send(embed=embed)
        else:
            await ctx.reply("I couldn't find any pictures of #" + bracelet_id + ", sorry about that.",
                            mention_author=False)

    # These both handle ID inputs that aren't numbers
    @id.error
    async def id_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("ID must be a number!")

    @pre.error
    async def pre_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("ID must be a number!")


def setup(bot):
    bot.add_cog(Bracelets(bot))

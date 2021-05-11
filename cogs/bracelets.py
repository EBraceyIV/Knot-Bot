import discord
from discord.ext import commands
import bs4
from cogs.html import *
import random


# This gets reused often so it's a function
def embed_init(bracelet_id, style, crafter, variations, url):
    # The "if not variations" statement accounts for pre and pic where variations are not needed for output
    # and "variations" is given as None to this function
    description = style + crafter[0].getText() + "." if not variations else \
        style + crafter[0].getText() + ".\n" + "Variations: " + variations
    embed = discord.Embed(title="Pattern #" + bracelet_id,
                          color=0xf7633f,
                          description=description,
                          url=url)
    embed.set_footer(text="Please DM my owner, Kiwi Shark, with questions/comments/concerns regarding my services.")
    return embed


def embed_extras(embed, crafter, crafter_url, crafter_icon):
    embed.set_author(name=crafter[0].getText(),
                     url=crafter_url[0].get("href"), icon_url=crafter_icon[0].get("src"))
    embed.set_thumbnail(url="https://static.braceletbookcdn.com/images/logo_header.png")
    return embed


def id_processing(bracelet_id):
    #  ID taken in as a string in case the user adds "#" to the start of the ID, as is sometimes common
    if bracelet_id[0] == "#":
        bracelet_id = bracelet_id[1:]

    # Check to see if the input is a number, provide a specific response if it isn't
    try:
        int(bracelet_id)
    except ValueError:
        # Raising this exception lets the response be sent via the command error events, so this function doesn't have
        # to be an async function
        raise commands.BadArgument

    # get_html function returns "valid_id, pattern_info, style, url"
    valid_id, pattern_info, style, url = get_html(bracelet_id)
    return valid_id, pattern_info, style, url, bracelet_id


class Bracelets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Display information about a pattern given its #ID
    @commands.command(name="id",
                      help="Provide a pattern ID from BB and get some info in the design!")
    async def id(self, ctx, bracelet_id):

        valid_id, pattern_info, style, url, bracelet_id = id_processing(bracelet_id)

        if valid_id:
            # Gather all of the parts of the embed message
            braceletSoup = bs4.BeautifulSoup(pattern_info.text, "html.parser")
            crafter, crafter_icon, crafter_url = crafter_info(braceletSoup)
            dims, strings, colors, variations = pattern_data(braceletSoup)
            variations = "0" if variations == [] else variations[0].getText()
            # "preview" is what the pattern looks like, whereas "pattern" is the actual knotting pattern
            preview = braceletSoup.select(".preview_svg img")
            pattern = braceletSoup.select(".pattern_image img")

            # Build the embed message
            embed = embed_init(bracelet_id, style, crafter, variations, url)
            embed.set_author(name=crafter[0].getText(),
                             url=crafter_url[0].get("href"), icon_url=crafter_icon[0].get("src"))
            embed.set_thumbnail(url=pattern[0].get("src"))
            embed.add_field(name="Dimensions", value=dims[0].getText())
            embed.add_field(name="Strings", value=strings[0].getText())
            embed.add_field(name="Colors", value=colors[0].getText())
            embed.set_image(url=preview[0].get("src"))

            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply("I couldn't find #" + bracelet_id + ", sorry about that.", mention_author=False)

    # Preview a finished bracelet
    @commands.command(name="pre",
                      help="Provide a pattern ID from BB and get a preview of a finished bracelet.")
    async def pre(self, ctx, bracelet_id):

        valid_id, pattern_info, style, url, bracelet_id = id_processing(bracelet_id)

        if valid_id:
            # Gather all of the parts of the embed message
            braceletSoup = bs4.BeautifulSoup(pattern_info.text, "html.parser")
            crafter, crafter_icon, crafter_url = crafter_info(braceletSoup)
            preview = braceletSoup.select(".preview_svg img")

            # Build the embed message
            embed = embed_init(bracelet_id, style, crafter, None, url)
            embed = embed_extras(embed, crafter,  crafter_url, crafter_icon)
            embed.set_image(url=preview[0].get("src"))

            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply("I couldn't find #" + bracelet_id + ", sorry about that.", mention_author=False)

    @commands.command(name="pic",
                      help="See a picture of a completed bracelet for a certain pattern!")
    async def pic(self, ctx, bracelet_id):

        valid_id, pattern_info, style, url, bracelet_id = id_processing(bracelet_id)
        print("CHECK 0")
        if valid_id:
            # Gather all of the parts of the embed message
            braceletSoup = bs4.BeautifulSoup(pattern_info.text, "html.parser")
            crafter, crafter_icon, crafter_url = crafter_info(braceletSoup)
            pictures = braceletSoup.select(".photos_item > a")
            print("CHECK 1")
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
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply("I couldn't find any pictures of #" + bracelet_id + ", sorry about that.",
                            mention_author=False)

    # These handle ID inputs that aren't numbers
    @id.error
    @pre.error
    @pic.error
    async def id_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("ID must be a number!", mention_author=False)


def setup(bot):
    bot.add_cog(Bracelets(bot))

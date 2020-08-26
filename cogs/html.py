from discord.ext import commands
import requests


# Get bracelet HTML
def get_html(bracelet_id):
    #  Converts the input to a string for clarity in use later,
    #  if the command runs then we know it's an int as the input should be
    bracelet_id = str(bracelet_id)
    # Check both url options, normal and alpha
    urls = ['https://www.braceletbook.com/patterns/normal/' + bracelet_id + '/',
            'https://www.braceletbook.com/patterns/alpha/' + bracelet_id + '/']
    # urls = ['https://www.braceletbook.com/variations/normal/' + bracelet_id + '/',
    #         'https://www.braceletbook.com/variations/alpha/' + bracelet_id + '/']
    # Using the exception given by get() in requests, determine if the pattern is a normal or an alpha
    try:
        # Get the page data if the pattern is a normal
        requests.get(urls[0]).raise_for_status()
        pattern_info = requests.get(urls[0])
        url = urls[0]
        style = 'This is a normal pattern created by '
    except Exception as eNormal:  # Pattern is not a normal
        try:
            # Get the page data if the pattern is an alpha
            requests.get(urls[1]).raise_for_status()
            pattern_info = requests.get(urls[1])
            url = urls[1]
            style = 'This is an alpha pattern created by '
        except Exception as eAlpha:  # Pattern can't be found
            return False, None, None, None
    return True, pattern_info, style, url


# Grab info about the crafter who made the bracelet
def crafter_info(braceletSoup):
    crafter = braceletSoup.select('.pattern_id_added_by .pattern_added_by')
    crafter_icon = braceletSoup.select('.pattern_id_added_by .pattern_added_by img')
    crafter_url = braceletSoup.select('.pattern_id_added_by .pattern_added_by a')
    return crafter, crafter_icon, crafter_url


# Grab info about the bracelet's properties
def pattern_data(braceletSoup):
    dims = braceletSoup.select('.pattern_dimensions .data')
    strings = braceletSoup.select('.pattern_strings .data')
    colors = braceletSoup.select('.pattern_colors .data')
    variations = braceletSoup.select('.variations .caption_orange')
    return dims, strings, colors, variations


class html(commands.Cog):
    # Lore commands always take the title of the lore first

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(html(bot))

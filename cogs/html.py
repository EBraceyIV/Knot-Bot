from discord.ext import commands
import requests


# Get bracelet HTML
def get_html(bracelet_id):
    # For potential use in scraping variations at some point
    # urls = ["https://www.braceletbook.com/variations/normal/" + bracelet_id + "/",
    #         "https://www.braceletbook.com/variations/alpha/" + bracelet_id + "/"]

    # Using the exception given by get() in requests, determine if the pattern is a normal or an alpha
    try:
        # Get the page data if the pattern is a normal
        requests.get("https://www.braceletbook.com/patterns/normal/" + bracelet_id + "/").raise_for_status()
        pattern_info, url, style = html_alphanorm(bracelet_id, "normal")
    except requests.exceptions.HTTPError:  # Pattern is not a normal
        try:
            # Get the page data if the pattern is an alpha
            requests.get("https://www.braceletbook.com/patterns/alpha/" + bracelet_id + "/").raise_for_status()
            pattern_info, url, style = html_alphanorm(bracelet_id, "alpha")
        except requests.exceptions.HTTPError:  # Pattern can't be found
            return False, None, None, None
    # Return HTML data for pattern information, what style the pattern is, and the pattern url
    return True, pattern_info, style, url


# HTML scraping helper function to handle normals vs alphas
def html_alphanorm(bracelet_id, normal_or_alpha):
    # Pattern URL built based on the pattern style
    url = "https://www.braceletbook.com/patterns/" + normal_or_alpha + "/" + bracelet_id + "/"
    # The HTML data for the pattern requested
    pattern_info = requests.get(url)
    # Flavor text to describe the pattern style to be used in the output
    style = "This is a " + normal_or_alpha + " pattern created by "
    return pattern_info, url, style


# Grab info about the crafter who made the bracelet
def crafter_info(braceletSoup):
    crafter = braceletSoup.select(".pattern_id_added_by .pattern_added_by")
    crafter_icon = braceletSoup.select(".pattern_id_added_by .pattern_added_by img")
    crafter_url = braceletSoup.select(".pattern_id_added_by .pattern_added_by a")
    return crafter, crafter_icon, crafter_url


# Grab info about the bracelet's properties
def pattern_data(braceletSoup):
    dims = braceletSoup.select(".pattern_dimensions .data")
    strings = braceletSoup.select(".pattern_strings .data")
    colors = braceletSoup.select(".pattern_colors .data")
    variations = braceletSoup.select(".variations .caption_orange")
    return dims, strings, colors, variations


class html(commands.Cog):
    # Lore commands always take the title of the lore first

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(html(bot))

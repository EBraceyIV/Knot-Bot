from discord.ext import commands
import random

# Pre-made lists used to reply to posts
autoReactEmoji = ["🎉", "👍", "✨", "💖", "🤩", "🧵", "😍", "❤", "🔥", "🌟"]
autoWIPReply = ["Looking great so far 💪", "Loving the colors 😍",
                "Very nice so far, can't wait for it to be finished!", "Keep up the hard work 🙌",
                "Oooo how much more of that do you have left to do? So far so good!"]
autoCompleteReply = ["Wowowowowow ✨✨✨", "Love those colors 😍", "Well done!!!", "That's great! How do you do it??",
                     "It looks so good 😍", "Super cute! 🤩"]


# This cog is dedicated to conducting automatic actions
class Auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Process incoming messages from channels for WIP and finished bracelet photos, give some encouragement
    @commands.Cog.listener()
    async def on_message(self, message):
        # Check for photos sent in the designated channels
        # Finished bracelets: 724448213955903550, WIP bracelets: 724449447391657995
        # Test channels: 627279552997228545 & 720833461329461347
        if message.attachments is not None and message.channel.id in [724448213955903550, 724449447391657995]:
            # In case of multiple attachments being posted at once in a message in order to process each individually
            for attachment in message.attachments:
                # Only process photos
                if attachment.filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".PNG", ".JPG", ".JPEG", ".GIF")):
                    # Every photo gets two fun emoji reactions selected from a defined list
                    for reaction in random.choices(autoReactEmoji, k=2):
                        await message.add_reaction(reaction)
                    # Every few photos send an encouraging text reply as a bonus
                    if random.randint(1, 4) == 1:
                        # Replies to "completed" photos from defined list
                        if message.channel.id == 724448213955903550:
                            await message.channel.send(random.choice(autoCompleteReply))
                        # Replies to "work-in-progress" photos from define list
                        elif message.channel.id == 724449447391657995:
                            await message.channel.send(random.choice(autoWIPReply))


# Add the cog
def setup(bot):
    bot.add_cog(Auto(bot))

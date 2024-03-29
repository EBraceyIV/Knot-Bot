from discord.ext import commands
import random

# Pre-made lists used to reply to posts
autoReactEmoji = ["🎉", "👍", "✨", "💖", "🤩", "🧵", "😍", "❤", "🔥", "🌟"]
autoWIPReply = ["Looking great so far 💪", "Loving the colors 😍",
                "Very nice!", "Keep up the hard work 🙌", "So far so good!", "Coming together nicely I see"]
autoCompleteReply = ["Wowowowowow ✨✨✨", "Love those colors 😍", "Well done!!!", "Wonderful!",
                     "It looks so good 😍", "Super cute! 🤩",
                     "I wish I could make something that nice, I'm just a bot though 🤖"]


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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.author == self.bot.user:
            if reaction.emoji == "🗑️":
                request_msg = await self.bot.get_channel(reaction.message.reference.channel_id)\
                    .fetch_message(reaction.message.reference.message_id)
                if user == request_msg.author:
                    await reaction.message.delete()
                    await request_msg.delete()


# Add the cog
async def setup(bot):
    await bot.add_cog(Auto(bot))

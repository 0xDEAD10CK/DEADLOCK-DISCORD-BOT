import discord
from discord.ext import commands
import os

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_channel_id = 1339687653754404934  # Replace with your channel ID as an integer
        self.verified_role_id = 123456789012345678  # Replace with your verified role ID as an integer

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Verification Cog has loaded!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bot messages

        if message.content.startswith('!verify'):
            await message.author.send(
                "Please upload two images for verification: an ID card and a selfie.\n"
                "You may edit the images to hide sensitive information but make sure the Date of Birth is visible on the ID card.\n"
                "Please make sure the two images are in the same message.\n\n"
                "This data will be used for verification purposes only and will be deleted after verification."
            )

        elif isinstance(message.channel, discord.DMChannel):  # Only process DMs
            image_attachments = [
                attachment for attachment in message.attachments
                if attachment.content_type and attachment.content_type.startswith('image/')
            ]

            if len(image_attachments) == 2:
                verification_channel = self.bot.get_channel(self.verification_channel_id)
                print(verification_channel)

                if verification_channel:
                    files = [await attachment.to_file() for attachment in image_attachments]
                    verifier_message = await verification_channel.send(
                        content=f"Verification request from {message.author.mention} (ID: {message.author.id})",
                        files=files
                    )

                    await verifier_message.add_reaction("✅")
                    await verifier_message.add_reaction("❌")

                    await message.channel.send("Your images have been forwarded to the Verifiers!")
                    await message.channel.send("Thanks for your message! We'll get back to you soon.")
                else:
                    await message.channel.send("Could not find the private verification channel.")
            else:
                await message.channel.send("Please upload exactly two images in the same message for verification.")

            await message.delete(delay=5)  # Delete the message after 5 seconds

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self.verification_channel_id:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member.bot:
                return  # Ignore bot reactions

            if str(payload.emoji) == "✅":
                role = guild.get_role(self.verified_role_id)
                if role:
                    await member.add_roles(role)
                    await member.send("You have been verified and the verified role has been added to you.")
            elif str(payload.emoji) == "❌":
                await member.send("Your verification request has been denied. Please contact the moderators for more information.")

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))

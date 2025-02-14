import discord
from discord.ext import commands
import os
import time

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rules_channel_id = os.getenv("RULES_CHANNEL_ID")  # Replace with your channel ID as an integer
        self.verification_channel_id = os.getenv("VERIFICATION_CHANNEL_ID")  # Replace with your channel ID as an integer
        self.verified_role_id = os.getenv("VERIFIED_ROLE_ID")  # Replace with your verified role ID as an integer
        self.guild_id = os.getenv("GUILD_ID")  # Replace with your guild ID as an integer

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Verification Cog has loaded!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bot messages

        elif isinstance(message.channel, discord.DMChannel):  # Only process DMs
            image_attachments = [
                attachment for attachment in message.attachments
                if attachment.content_type and attachment.content_type.startswith('image/')
            ]

            if len(image_attachments) == 2:
                verification_channel = self.bot.get_channel(int(self.verification_channel_id))
                print(verification_channel)

                if verification_channel:
                    files = [await attachment.to_file() for attachment in image_attachments]
                    verifier_message = await verification_channel.send(
                        content=f"Verification request from {message.author.mention} (ID: {message.author.id})",
                        files=files
                    )

                    await verifier_message.add_reaction("✅")
                    await verifier_message.add_reaction("❌")

                    # Store the user ID in the message metadata
                    verifier_message.author_id = message.author.id

                    await message.channel.send("Your images have been forwarded to the Verifiers!")
                    await message.channel.send("Thanks for your message! We'll get back to you soon.")
                else:
                    await message.channel.send("Could not find the private verification channel.")
            else:
                await message.channel.send("Please upload exactly two images in the same message for verification.")

            await message.delete(delay=5)  # Delete the message after 5 seconds

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == int(self.rules_channel_id):
            print('DEBUG: Reaction added in rules channel')
            print(f"DEBUG: Emoji name -> {repr(payload.emoji.name)}")

            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            print(f"DEBUG: Member -> {member}") # Debug

            if member and member.bot:
                return  # Ignore bot reactions
            
            await member.send(
                "Please upload two images for verification: an ID card and a selfie.\n"
                "You may edit the images to hide sensitive information but make sure the Date of Birth is visible on the ID card.\n"
                "Please make sure the two images are in the same message.\n\n"
                "This data will be used for verification purposes only and will be deleted after verification."
            )


        if payload.channel_id == int(self.verification_channel_id):
            print('DEBUG: Reaction added in verification channel')
            print(f"DEBUG: Emoji name -> {repr(payload.emoji.name)}")

            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            if member and member.bot:
                return  # Ignore bot reactions

            # Fetch the message that was reacted to
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            if not message or not message.content:
                print("DEBUG: Message not found or has no content")
                return

            # Extract the user ID from the message content
            import re
            match = re.search(r"\(ID: (\d+)\)", message.content)
            if not match:
                print("DEBUG: Could not extract user ID from message.")
                return

            user_id = int(match.group(1))
            user = guild.get_member(user_id)
            if not user:
                print(f"DEBUG: Could not find user with ID {user_id}")
                return

            # Get the verification role
            #role = guild.get_role(int(self.verified_role_id))
            role = discord.utils.get(guild.roles, name="Verified")
            if not role:
                print("DEBUG: Could not find the verified role.")
                return

            # Handle verification decision
            if payload.emoji.name == "✅":
                print(f'DEBUG: Verifying user {user}, adding role {role}')
                await user.add_roles(role)
                await user.send("You have been verified and the verified role has been added to you.")

            elif payload.emoji.name == "❌":
                print(f'DEBUG: Denying verification for user {user}')
                await user.send("Your verification request has been denied. Please contact the moderators for more information.")

            time.sleep(5)
            await message.delete()

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))
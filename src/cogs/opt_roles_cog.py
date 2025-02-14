import discord
from discord.ext import commands
import dotenv
import os
import datetime as dt

class ReactRolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_channel_id = os.getenv('ROLES_CHANNEL_ID')
        self.owner_id = os.getenv('OWNER_ID')
        self.role_dict = {
                    "🩷": "she/her",
                    "💙": "he/him",
                    "💛": "they/them",
                    "1️⃣": "18-24",
                    "2️⃣": "25-30",
                    "3️⃣": "31-44",
                    "4️⃣": "45+",
                    "🖥️": "PC",
                    "🎮": "Xbox",
                    "🎰": "Playstation",
                    "🕹️": "Nintendo Switch",
                    "🤍": "Single",
                    "💚": "Taken",
                    "🖤": "Complicated",
                    "💜": "Open Relationship",
                    "👀": "Poly/Looking",
                    "🙅🏽": "Poly/Not Looking",
                    "😏": "Poly/Flirting",
                    "📱": "Open Dms",
                    "❓": "Ask to Dm",
                    "🤫": "Closed Dms",
                    "📖": "Booktok Thot",
                    "🫦": "Flirting",
                    "🙉": "No Flirting",
                    "🐺": "Feral"
                }

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Reaction Roles Cog has loaded!')


    @commands.command(name='create_reaction_role_channel')
    async def create_reaction_role_channel(self, ctx):
        '''Creates the reaction role channel'''

        # Check if command is run by only me
        if ctx.author.id != self.owner_id:
            await ctx.send("You do not have permission to run this command.")
            return

        guild = ctx.guild

        # get roles text channel
        channel = discord.utils.get(guild.text_channels, name="get-roles")

        # Send messages and store them in variables
        gender_message = await channel.send(
            "React to the messages below to get the corresponding roles: \n\n"
            "she/her - 🩷 \n"
            "he/him - 💙 \n"
            "they/them - 💛 \n\n"
        )

        age_message = await channel.send(
            "18-24 - 1️⃣ \n"
            "25-30 - 2️⃣ \n"
            "31-44 - 3️⃣ \n"
            "45+ - 4️⃣ \n\n"
        )

        platform_message = await channel.send(
            "PC - 🖥️ \n"
            "Xbox - 🎮 \n"
            "Playstation - 🎰 \n"
            "Nintendo Switch - 🕹️ \n\n"
        )

        relationship_message = await channel.send(
            "Single - 🤍 \n"
            "Taken - 💚 \n"
            "Complicated - 🖤 \n"
            "Open Relationship - 💜 \n"
            "Poly/Looking - 👀 \n"
            "Poly/Not Looking - 🙅🏽 \n"
            "Poly/Flirting - 😏 \n\n"
        )

        dm_message = await channel.send(
            "Open Dms - 📱 \n"
            "Ask to Dm - ❓ \n"
            "Closed Dms - 🤫 \n"
            "Booktok Thot - 📖 \n"
            "Flirting - 🫦 \n"
            "No flirting - 🙉 \n"
            "Feral - 🐺 \n\n"
        )

        # Define dictionaries for role assignments
        gender_roles = {
            "🩷": "she/her",
            "💙": "he/him",
            "💛": "they/them"
        }

        age_roles = {
            "1️⃣": "18-24",
            "2️⃣": "25-30",
            "3️⃣": "31-44",
            "4️⃣": "45+"
        }

        platform_roles = {
            "🖥️": "PC",
            "🎮": "Xbox",
            "🎰": "Playstation",
            "🕹️": "Nintendo Switch"
        }

        relationship_roles = {
            "🤍": "Single",
            "💚": "Taken",
            "🖤": "Complicated",
            "💜": "Open Relationship",
            "👀": "Poly/Looking",
            "🙅🏽": "Poly/Not Looking",
            "😏": "Poly/Flirting"
        }

        dm_roles = {
            "📱": "Open Dms",
            "❓": "Ask to Dm",
            "🤫": "Closed Dms",
            "📖": "Booktok Thot",
            "🫦": "Flirting",
            "🙉": "No Flirting",
            "🐺": "Feral"
        }

        # Add reactions to each message
        role_messages = [
            (gender_message, gender_roles),
            (age_message, age_roles),
            (platform_message, platform_roles),
            (relationship_message, relationship_roles),
            (dm_message, dm_roles)
        ]

        for message, roles in role_messages:
            for emoji, role_name in roles.items():
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    role = await guild.create_role(name=role_name)
                await message.add_reaction(emoji)

        await ctx.send("Reaction roles channel created successfully!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        '''Listens for when the user adds a reaction to
          a message in the reaction channel.'''

        # Check if the reaction is in the "get-roles" channel
        if str(payload.channel_id) == self.roles_channel_id:
            guild = self.bot.get_guild(payload.guild_id)

            member = guild.get_member(payload.user_id)
            if member is None:  # Sometimes member might be None if it's not in cache
                member = await guild.fetch_member(payload.user_id)

            if member.bot:
                return  # Ignore bot reactions

            # Get the role name based on the emoji used
            role_name = self.role_dict.get(str(payload.emoji))

            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    await member.add_roles(role)
                    print(f"[{dt.datetime.now()}] Added {role_name} role to {member.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        '''Listens for when the user removes a
         reaction from a message in the reaction channel.'''

        if str(payload.channel_id) == self.roles_channel_id:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if member is None:  # Sometimes member might be None if it's not in cache
                member = await guild.fetch_member(payload.user_id)
            if member.bot:
                return  # Ignore bot reactions

            # Get the role name based on the emoji used
            role_name = self.role_dict.get(str(payload.emoji))
            if role_name:
                role = discord.utils.get(guild.roles, name=role_name)
                if role:
                    await member.remove_roles(role)
                    print(f"[{dt.datetime.now()}] Removed {role_name} role from {member.name}")


async def setup(bot):
    await bot.add_cog(ReactRolesCog(bot))

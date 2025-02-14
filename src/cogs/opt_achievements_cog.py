import discord
from discord.ext import commands
import json
import os

class AchievementsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.achievements_file = "achievements.json"
        self.achievements = self.load_achievements()

    def load_achievements(self):
        """Load achievements from a JSON file or create a new one."""
        if os.path.exists(self.achievements_file):
            with open(self.achievements_file, "r") as f:
                return json.load(f)
        return {}

    def save_achievements(self):
        """Save achievements to a JSON file."""
        with open(self.achievements_file, "w") as f:
            json.dump(self.achievements, f, indent=4)

    def add_achievement(self, user_id, achievement_name):
        """Unlock an achievement for a user."""
        user_id = str(user_id)  # Convert to string for JSON compatibility
        if user_id not in self.achievements:
            self.achievements[user_id] = []

        if achievement_name not in self.achievements[user_id]:
            self.achievements[user_id].append(achievement_name)
            self.save_achievements()
            return True  # New achievement unlocked
        return False  # Achievement already unlocked

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[ WORKING ] - Achievements Cog has loaded!")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Track achievements based on message activity."""
        if message.author.bot:
            return

        user_id = message.author.id

        # Example: Unlock an achievement for sending first message
        if self.add_achievement(user_id, "First Message"):
            await message.channel.send(f"🎉 {message.author.mention} unlocked: **First Message!**")

        # Example: Unlock an achievement for sending 100 messages
        user_messages = sum(len(v) for v in self.achievements.values())
        if user_messages >= 100 and self.add_achievement(user_id, "Chatterbox"):
            await message.channel.send(f"🎉 {message.author.mention} unlocked: **Chatterbox!**")

    @commands.command(name="achievements")
    async def achievements(self, ctx):
        """Display user's unlocked achievements."""
        user_id = str(ctx.author.id)
        user_achievements = self.achievements.get(user_id, [])

        if not user_achievements:
            await ctx.send(f"{ctx.author.mention}, you haven't unlocked any achievements yet!")
        else:
            achievement_list = "\n".join([f"✅ {a}" for a in user_achievements])
            embed = discord.Embed(
                title=f"{ctx.author.name}'s Achievements",
                description=achievement_list,
                color=discord.Color.gold(),
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AchievementsCog(bot))

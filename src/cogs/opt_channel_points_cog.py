import discord
from discord.ext import commands, tasks
import json
import os
import asyncio

class ChannelPointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.points_file = 'points.json'
        self.points = self.load_points()
        self.lock = asyncio.Lock()
        self.user_message_counts = {}
        self.message_threshold = 5  # Grant points every 5 messages
        self.passive_reward.start()

        print("[DEBUG] ChannelPointsCog initialized.")

    def load_points(self):
        """Loads points from file."""
        if os.path.exists(self.points_file):
            with open(self.points_file, 'r') as file:
                try:
                    print("[DEBUG] Loading points from file...")
                    return json.load(file)
                except json.JSONDecodeError:
                    print("[ERROR] Failed to decode points.json, resetting points.")
                    return {}
        print("[DEBUG] No points file found, initializing empty points dictionary.")
        return {}

    async def save_points(self):
        """Saves points to file."""
        async with self.lock:
            try:
                with open(self.points_file, 'w') as file:
                    json.dump(self.points, file)
                print("[DEBUG] Points successfully saved.")
            except Exception as e:
                print(f"[ERROR] Failed to save points: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[ BROKEN ] - Channel Points Cog has loaded!")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handles message-based point rewards."""
        if message.author.bot:
            return  # Ignore bot messages

        user_id = str(message.author.id)
        async with self.lock:
            self.user_message_counts[user_id] = self.user_message_counts.get(user_id, 0) + 1
            print(f"[DEBUG] {message.author} sent a message. Total messages: {self.user_message_counts[user_id]}")

            if self.user_message_counts[user_id] >= self.message_threshold:
                self.points[user_id] = self.points.get(user_id, 0) + 1
                self.user_message_counts[user_id] = 0
                print(f"[DEBUG] {message.author} earned a point! New total: {self.points[user_id]}")
                await self.save_points()

    @tasks.loop(minutes=10)
    async def passive_reward(self):
        """Gives 2 points every 10 minutes to active users."""
        print("[DEBUG] Running passive rewards task...")
        async with self.lock:
            for user_id in self.user_message_counts.keys():
                self.points[user_id] = self.points.get(user_id, 0) + 2
                print(f"[DEBUG] {user_id} received passive points. New total: {self.points[user_id]}")
            await self.save_points()

    @commands.command(name='points')
    async def check_points(self, ctx):
        """Check user points."""
        user_id = str(ctx.author.id)
        async with self.lock:
            points = self.points.get(user_id, 0)
        print(f"[DEBUG] {ctx.author} checked points. Total: {points}")
        await ctx.send(f'{ctx.author.mention}, you have {points} points.')

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """Displays the top 10 users with the most points."""
        async with self.lock:
            sorted_points = sorted(self.points.items(), key=lambda x: x[1], reverse=True)[:10]

        if not sorted_points:
            await ctx.send("No one has earned any points yet!")
            return

        leaderboard_text = '\n'.join([f"<@{user}>: {points}" for user, points in sorted_points])
        print("[DEBUG] Leaderboard requested.")
        await ctx.send(f'**Top 10 Leaderboard:**\n{leaderboard_text}')

    @commands.command(name='add_points')
    @commands.has_permissions(administrator=True)
    async def add_points(self, ctx, member: discord.Member, points: int):
        """Allows admins to add points to a user."""
        user_id = str(member.id)
        async with self.lock:
            self.points[user_id] = self.points.get(user_id, 0) + points
            await self.save_points()
        print(f"[DEBUG] {ctx.author} added {points} points to {member}. New total: {self.points[user_id]}")
        await ctx.send(f'{points} points have been added to {member.mention}.')

    @commands.command(name='remove_points')
    @commands.has_permissions(administrator=True)
    async def remove_points(self, ctx, member: discord.Member, points: int):
        """Allows admins to remove points from a user."""
        user_id = str(member.id)
        async with self.lock:
            self.points[user_id] = max(self.points.get(user_id, 0) - points, 0)
            await self.save_points()
        print(f"[DEBUG] {ctx.author} removed {points} points from {member}. New total: {self.points[user_id]}")
        await ctx.send(f'{points} points have been removed from {member.mention}.')

    @commands.command(name='transfer_points')
    async def transfer_points(self, ctx, member: discord.Member, points: int):
        """Allows users to transfer points to others."""
        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)

        async with self.lock:
            sender_points = self.points.get(sender_id, 0)
            if sender_points < points:
                print(f"[ERROR] {ctx.author} tried to transfer {points} points but only has {sender_points}.")
                await ctx.send(f'{ctx.author.mention}, you do not have enough points to transfer!')
                return

            self.points[sender_id] -= points
            self.points[receiver_id] = self.points.get(receiver_id, 0) + points
            await self.save_points()

        print(f"[DEBUG] {ctx.author} transferred {points} points to {member}.")
        await ctx.send(f'{ctx.author.mention} has transferred {points} points to {member.mention}!')

async def setup(bot):
    print("[DEBUG] Setting up ChannelPointsCog...")
    await bot.add_cog(ChannelPointsCog(bot))
    print("[DEBUG] ChannelPointsCog has been added to the bot.")

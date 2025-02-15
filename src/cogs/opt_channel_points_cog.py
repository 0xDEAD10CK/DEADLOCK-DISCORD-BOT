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
        self.save_lock = asyncio.Lock()
        self.message_lock = asyncio.Lock()
        self.check_points_lock = asyncio.Lock()
        self.add_points_lock = asyncio.Lock()
        self.remove_points_lock = asyncio.Lock()
        self.reward_lock = asyncio.Lock()
        self.transfer_points_lock = asyncio.Lock()
        self.leaderboard_lock = asyncio.Lock()
        self.user_message_counts = {}
        self.message_threshold = 5  # Grant points every 5 messages

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
        with open(self.points_file, 'w') as file:
            json.dump({}, file)
            file.close()

        return {}

    async def save_points(self):
        """Saves points to file."""
        async with self.save_lock:
            try:
                print("[DEBUG] Acquired lock in save_points")
                with open(self.points_file, 'w') as file:
                    json.dump(self.points, file)
                print("[DEBUG] Points successfully saved.")
            except Exception as e:
                print(f"[ERROR] Failed to save points: {e}")
            finally:
                print("[DEBUG] Released lock in save_points")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[ WORKING ] - Channel Points Cog has loaded!")
        if not self.passive_reward.is_running():
            self.passive_reward.start()
            print("[DEBUG] Passive reward task started.")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handles message-based point rewards."""

        if message.author.bot:
            return  # Ignore bot messages

        user_id = str(message.author.id)

        print(f"[DEBUG] {message.author} sent a message.")

        print(f'[DEBUG] Passive Reward Task: {self.passive_reward.is_running()}')

        async with self.message_lock:
            print("[DEBUG] Acquired lock in on_message")
            self.user_message_counts[user_id] = self.user_message_counts.get(user_id, 0) + 1
            print(f"[DEBUG] {message.author} sent a message. Total messages: {self.user_message_counts[user_id]}")

            if self.user_message_counts[user_id] >= self.message_threshold:
                self.points[user_id] = self.points.get(user_id, 0) + 1
                self.user_message_counts[user_id] = 0
                print(f"[DEBUG] {message.author} earned a point! New total: {self.points[user_id]}")
                await self.save_points()
            print("[DEBUG] Released lock in on_message")
    
    #
    # Error in loop somewhere. Passing through loop and not updating points.
    #
    
    @tasks.loop(seconds=10.0)
    async def passive_reward(self):
        """Gives 2 points every 10 seconds to active users for debug purposes."""
        print("[DEBUG] Running passive rewards task...")
        async with self.reward_lock:
            print("[DEBUG] Acquired lock in passive_reward")
            for user_id in self.user_message_counts.keys():
                self.points[user_id] = self.points.get(user_id, 0) + 2
                print(f"[DEBUG] {user_id} received passive points. New total: {self.points[user_id]}")
            await self.save_points()
            print("[DEBUG] Released lock in passive_reward")

    @passive_reward.before_loop
    async def before_passive_reward(self):
        await self.bot.wait_until_ready()
        print("[DEBUG] Waiting until bot is ready before starting passive rewards task...")

    @commands.command(name='points')
    async def check_points(self, ctx):
        """Check user points."""
        user_id = str(ctx.author.id)
        print(f"[ DEBUG ] {ctx.author.name} Checking points...")
        async with self.check_points_lock:
            print("[DEBUG] Acquired lock in check_points")
            points = self.points.get(user_id, 0)
        print(f"[DEBUG] {ctx.author} checked points. Total: {points}")
        await ctx.send(f'{ctx.author.mention}, you have {points} points.')
        print("[DEBUG] Released lock in check_points")

    @commands.command(name='leaderboard')
    async def leaderboard(self, ctx):
        """Displays the top 10 users with the most points."""
        async with self.leaderboard_lock:
            print("[DEBUG] Acquired lock in leaderboard")
            sorted_points = sorted(self.points.items(), key=lambda x: x[1], reverse=True)[:10]

        if not sorted_points:
            await ctx.send("No one has earned any points yet!")
            return

        leaderboard_text = '\n'.join([f"<@{user}>: {points}" for user, points in sorted_points])
        print("[DEBUG] Leaderboard requested.")
        await ctx.send(f'**Top 10 Leaderboard:**\n{leaderboard_text}')
        print("[DEBUG] Released lock in leaderboard")

    @commands.command(name='add_points')
    @commands.has_permissions(administrator=True)
    async def add_points(self, ctx, member: discord.Member, points: int):
        """Allows admins to add points to a user."""
        user_id = str(member.id)
        async with self.add_points_lock:
            print("[DEBUG] Acquired lock in add_points")
            self.points[user_id] = self.points.get(user_id, 0) + points
            await self.save_points()
        print(f"[DEBUG] {ctx.author} added {points} points to {member}. New total: {self.points[user_id]}")
        await ctx.send(f'{points} points have been added to {member.mention}.')
        print("[DEBUG] Released lock in add_points")

    @commands.command(name='remove_points')
    @commands.has_permissions(administrator=True)
    async def remove_points(self, ctx, member: discord.Member, points: int):
        """Allows admins to remove points from a user."""
        user_id = str(member.id)
        async with self.remove_points_lock:
            print("[DEBUG] Acquired lock in remove_points")
            self.points[user_id] = max(self.points.get(user_id, 0) - points, 0)
            await self.save_points()
        print(f"[DEBUG] {ctx.author} removed {points} points from {member}. New total: {self.points[user_id]}")
        await ctx.send(f'{points} points have been removed from {member.mention}.')
        print("[DEBUG] Released lock in remove_points")

    @commands.command(name='transfer_points')
    async def transfer_points(self, ctx, member: discord.Member, points: int):
        """Allows users to transfer points to others."""
        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)

        async with self.transfer_points_lock:
            print("[DEBUG] Acquired lock in transfer_points")
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
        print("[DEBUG] Released lock in transfer_points")

async def setup(bot):
    print("[DEBUG] Setting up ChannelPointsCog...")
    await bot.add_cog(ChannelPointsCog(bot))
    print("[DEBUG] ChannelPointsCog has been added to the bot.")
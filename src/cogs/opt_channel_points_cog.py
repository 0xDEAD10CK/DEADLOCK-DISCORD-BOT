import discord
from discord.ext import commands, tasks
import asyncio
import aiosqlite

class ChannelPointsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = 'points.db'
        self.save_lock = asyncio.Lock()
        self.message_lock = asyncio.Lock()
        self.reward_lock = asyncio.Lock()
        self.database_lock = asyncio.Lock()
        self.message_threshold = 5  # Grant points every 5 messages
        self.bot.loop.create_task(self.initialize_database())
        print("[DEBUG] ChannelPointsCog initialized.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("[DEBUG] ChannelPointsCog is ready.")
        await self.initialize_all_users()

    async def initialize_database(self):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS points (
                    user_id TEXT PRIMARY KEY,
                    points INTEGER NOT NULL
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS message_counts (
                    user_id TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
            ''')
            await db.commit()
        print("[DEBUG] Database initialized.")

    async def initialize_all_users(self):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS points (
                    user_id TEXT PRIMARY KEY,
                    points INTEGER NOT NULL
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS message_counts (
                    user_id TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
            ''')
            await db.commit()

        for guild in self.bot.guilds:
            for member in guild.members:
                user_id = str(member.id)
                async with aiosqlite.connect(self.db_file) as db:
                    await db.execute('''
                        INSERT INTO points (user_id, points) VALUES (?, 0)
                        ON CONFLICT(user_id) DO NOTHING
                    ''', (user_id,))
                    await db.execute('''
                        INSERT INTO message_counts (user_id, count) VALUES (?, 0)
                        ON CONFLICT(user_id) DO NOTHING
                    ''', (user_id,))
                    await db.commit()
        print("[DEBUG] All users initialized with 0 points and 0 message counts.")

    async def get_points(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute('SELECT points FROM points WHERE user_id = ?', (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def set_points(self, user_id, points):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                INSERT INTO points (user_id, points) VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET points = excluded.points
            ''', (user_id, points))
            await db.commit()

    async def get_message_count(self, user_id):
        async with aiosqlite.connect(self.db_file) as db:
            async with db.execute('SELECT count FROM message_counts WHERE user_id = ?', (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    async def set_message_count(self, user_id, count):
        async with aiosqlite.connect(self.db_file) as db:
            await db.execute('''
                INSERT INTO message_counts (user_id, count) VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET count = excluded.count
            ''', (user_id, count))
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bot messages

        user_id = str(message.author.id)
        print(f"[DEBUG] {message.author} sent a message.")

        async with self.message_lock:
            current_count = await self.get_message_count(user_id)
            new_count = current_count + 1
            await self.set_message_count(user_id, new_count)
            print(f"[DEBUG] {message.author} sent a message. Total messages: {new_count}")

            if new_count >= self.message_threshold:
                current_points = await self.get_points(user_id)
                await self.set_points(user_id, current_points + 1)
                await self.set_message_count(user_id, 0)
                print(f"[DEBUG] {message.author} earned a point! New total: {current_points + 1}")

    @commands.command(name='points')
    async def check_points(self, ctx):
        user_id = str(ctx.author.id)
        points = await self.get_points(user_id)
        await ctx.send(f'{ctx.author.mention}, you have {points} points.')

async def setup(bot):
    print("[DEBUG] Setting up ChannelPointsCog...")
    await bot.add_cog(ChannelPointsCog(bot))
    print("[DEBUG] ChannelPointsCog has been added to the bot.")
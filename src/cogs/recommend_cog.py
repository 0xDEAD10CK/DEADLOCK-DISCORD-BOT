import discord
from discord.ext import commands

class RecommendCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Raffle Cog has loaded!')

    @commands.command(name='recommend')
    async def recommend(self, ctx):
        await ctx.send('Hello! I am a Discord bot cog!')

async def setup(bot):
    await bot.add_cog(RecommendCog(bot))
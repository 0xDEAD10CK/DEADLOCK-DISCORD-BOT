import discord
from discord.ext import commands

class NasaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Example Cog has loaded!')

    @commands.command(name='apod')
    async def apod(self, ctx):
        await ctx.send('Hello! I am a Discord bot cog!')

async def setup(bot):
    await bot.add_cog(NasaCog(bot))

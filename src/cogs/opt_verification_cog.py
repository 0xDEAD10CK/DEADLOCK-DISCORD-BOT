import discord
from discord.ext import commands

class VerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Verification Cog has loaded!')

    @commands.command(name='verify')
    async def verify(self, ctx):
        await ctx.send('Hello! I am a Discord bot cog!')

async def setup(bot):
    await bot.add_cog(VerificationCog(bot))

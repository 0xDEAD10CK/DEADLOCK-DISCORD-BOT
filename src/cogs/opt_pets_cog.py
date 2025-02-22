import discord
from discord.ext import commands

class PetsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Pets Cog has loaded!')

    @commands.command(name='adopt')
    async def adopt(self, ctx):
        await ctx.send('Pet adopted!')

async def setup(bot):
    await bot.add_cog(PetsCog(bot))
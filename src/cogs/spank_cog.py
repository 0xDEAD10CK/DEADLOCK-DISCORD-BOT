import discord
import random
from discord.ext import commands
import datetime as dt

class SpankCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Spank Cog has loaded!')

    @commands.command(name='spank')
    async def spank(self, ctx):
        print(f'[{dt.datetime.now()}] {ctx.author} has spanked the bot!')
        responses = [
            "~Harder daddy~",
            "~Ouch~",
            "~That hurt~",
            "~I've been naughty~",
            "~I'm sorry~",
            "~I'll be good~",
            "~I'll be better~",
            "~I'll be your good girl~",
            "~Daddy?~",
            "~I'm sorry daddy~",
            "~Don't stop~"]
        await ctx.send(f"{random.choice(responses)}")

async def setup(bot):
    await bot.add_cog(SpankCog(bot))
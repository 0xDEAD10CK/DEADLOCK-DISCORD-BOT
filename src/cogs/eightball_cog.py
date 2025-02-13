import discord
from discord.ext import commands
import random
import datetime as dt

class EightballCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Eightball Cog has loaded!')

    @commands.command(name='eightball')
    async def eightball(self, ctx, question: str):
        '''Eightball command for getting random answers to questions.'''

        responses = ["Yes, definitely.", "No, never.", "Ask again later.", "Don't count on it.", "It is certain.",
                    "Very doubtful.", "Most likely.", "My sources say no.", "Outlook not so good.", "Yes, but not right now.",
                    "Cannot predict now.", "Without a doubt."]

        response = random.choice(responses)

        print(f'[{dt.datetime.now()}] {ctx.author} has asked a question!')
        await ctx.send(f"{ctx.author.mention}, {response}")

async def setup(bot):
    await bot.add_cog(EightballCog(bot))

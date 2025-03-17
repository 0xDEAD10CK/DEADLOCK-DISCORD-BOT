import discord
from discord.ext import commands
import random
import os
from utils.welcome_messages import welcome_messages

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel = os.getenv('WELCOME_CHANNEL_ID') 
        self.welcome_messages = welcome_messages


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Welcome Cog has loaded!')

    @commands.Cog.listener()    
    async def on_member_join(self, member):
        # Check if the welcome channel is set
        if self.welcome_channel:
            # Get the welcome channel
            welcome_channel = member.guild.get_channel(int(self.welcome_channel))
            # Send the welcome message to the welcome channel
            await welcome_channel.send(random.choice(self.welcome_messages).format(user=member.mention))

        # Test a random welcome message
    @commands.command(name='welcome_test')
    # Check if the user is the owner of the bot
    async def welcome_test(self, ctx):
         print(ctx.author.id)
         if self.welcome_channel:
            # Get the welcome channel
            welcome_channel = ctx.guild.get_channel(int(self.welcome_channel))

            # Send the welcome message to the welcome channel
            await welcome_channel.send(random.choice(self.welcome_messages).format(user=ctx.author.mention))


async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))

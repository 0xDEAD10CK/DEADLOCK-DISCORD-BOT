import discord
from discord.ext import commands, tasks

class RaffleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Raffle Cog has loaded!')

    @commands.command(name='raffle')
    async def raffle(self, ctx):
        # Create a raffle where users can react to enter.
        await ctx.send(f'Raffle time! React to enter.\nWinner will be chosen in 24 hours.\nThe prize is: {ctx.message.content}')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if the reaction is added to the raffle message.
        if 'Raffle time! React to enter.' in reaction.message.content:
            await reaction.message.channel.send(f'{user.name} has entered the raffle!')

    # use tasks to check for the winner after 24 hours
    # if there are no entries, delete the message
    # if there are entries, pick a winner and announce it
    # delete the message
    @tasks.loop(hours=24)
    async def check_winner(self):
        

        pass

async def setup(bot):
    await bot.add_cog(RaffleCog(bot))

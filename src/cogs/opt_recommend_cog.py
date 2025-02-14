import discord
from discord.ext import commands
import os

class RecommendCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = int(os.getenv('OWNER_ID'))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Recommendation Cog has loaded!')

    @commands.command(name='recommend')
    async def recommend(self, ctx, *, message_content: str):
        '''Recommend command for getting recommendations.'''
        owner = await self.bot.fetch_user(self.owner_id)

        print(ctx.message)

        # Send owner a message
        await owner.send(f'{ctx.author} has requested a recommendation!\n\nMessage: {message_content}')

async def setup(bot):
    await bot.add_cog(RecommendCog(bot))
import discord
from discord.ext import commands
import aiohttp
import os

class NasaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nasa_api_key = 'DEMO_KEY'

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - NASA Cog has loaded!')

    @commands.command(name='apod')
    async def apod(self, ctx):
        """Fetches the Astronomy Picture of the Day from NASA."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.nasa.gov/planetary/apod?api_key={self.nasa_api_key}') as response:
                if response.status == 200:
                    data = await response.json()
                    embed = discord.Embed(title=data['title'], description=data['explanation'], color=discord.Color.blue())
                    embed.set_image(url=data['url'])
                    embed.set_footer(text=f"Date: {data['date']}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Failed to fetch APOD data from NASA.')

async def setup(bot):
    await bot.add_cog(NasaCog(bot))

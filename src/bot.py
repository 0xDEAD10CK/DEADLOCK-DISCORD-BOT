import discord
from discord.ext import commands
import os
import dotenv

# Check if windows, change the windows title.
if os.name == 'nt':
	os.system('title' + 'Dungeon Master')

# Load the environment variables.
dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename.startswith('opt_'):
                ans = input(f'{filename[4:-3]} is an optional Cog. \nWould you like to add it? y/n:')
                if ans.lower() != 'y':
                    break

            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

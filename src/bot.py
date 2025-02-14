import discord
from discord.ext import commands
import os
import dotenv
import inquirer

# Check if windows, change the windows title.
if os.name == 'nt':
    os.system('title' + 'Dungeon Master')

# Load the environment variables.
dotenv.load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.dm_messages = True
intents.members = True
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def load_extensions():
    optional_cogs = [filename for filename in os.listdir('./cogs') if filename.startswith('opt_') and filename.endswith('.py')]
    questions = [
        inquirer.Checkbox(
            'cogs',
            message="Select the optional cogs you want to load",
            choices=[filename[4:-3] for filename in optional_cogs],
        ),
    ]
    answers = inquirer.prompt(questions)
    selected_cogs = answers['cogs'] if answers else []
                                 
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename.startswith('opt_') and filename[4:-3] not in selected_cogs:
                continue

            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

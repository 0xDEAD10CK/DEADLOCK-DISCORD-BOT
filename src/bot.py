import discord
from discord.ext import commands
import os
import dotenv
import inquirer
import json

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
    selected_cogs_file = 'selected_cogs.json'
    optional_cogs = [filename for filename in os.listdir('./cogs') if filename.startswith('opt_') and filename.endswith('.py')]

    if os.path.exists(selected_cogs_file):
        with open(selected_cogs_file, 'r') as file:
            selected_cogs = json.load(file)
        
        print(f"Previously selected cogs: {', '.join(selected_cogs)}")
        
        questions = [
            inquirer.List(
                'use_saved',
                message="Do you want to use the previously selected cogs?",
                choices=['Yes', 'No']
            ),
        ]
        answers = inquirer.prompt(questions)
        if answers['use_saved'] == 'No':
            selected_cogs = []
    else:
        selected_cogs = []

    if not selected_cogs:
        questions = [
            inquirer.Checkbox(
                'cogs',
                message="Select the optional cogs you want to load",
                choices=[filename[4:-3] for filename in optional_cogs],
            ),
        ]
        answers = inquirer.prompt(questions)
        selected_cogs = answers['cogs'] if answers else []

        with open(selected_cogs_file, 'w') as file:
            json.dump(selected_cogs, file)

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            if filename.startswith('opt_') and filename[4:-3] not in selected_cogs:
                continue

            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_token)
        os.system('clear')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

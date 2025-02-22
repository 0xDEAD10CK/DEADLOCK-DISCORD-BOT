import discord
import json
import os
import asyncio
import random
import datetime as dt
from discord.ext import commands

PET_DATA_FILE = "utils/pets.json"

class PetsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pets = self.load_pet_data()
        self.lock = asyncio.Lock()  # Prevent simultaneous writes
        self.pet_list = [
            "Drake",
            "Yeti",
            "Golem",
            "Gryphon",
            "Serpent",
            "Salamander",
            "Unicorn",
            "Wraith",
            "Sphinx",
            "Behemoth",
            "Minotaur",
            "Banshee",
            "Pegasus",
            "Hydra",
            "Phoenix",
            "Wendigo",
            "Treant",
            "Specter",
            "Chimera",
            "Wyrm",
            "Harpy",
            "Cerberus",
            "Kraken",
            "Leviathan",
            "Manticore",
            "Cyclops",
            "Griffin",
            "Basilisk",
            "Gorgon",
            "Siren",
            "Titan"
        ]
        self.type_list = [
            "Fire",
            "Ice",
            "Wind",
            "Water",
            "Earth",
            "Electric",
            "Solar",
            "Lunar",
            "Shadow",
            "Mystic",
            "Nature",
            "Astral",
            "Toxic",
            "Metallic",
            "Spectral",
            "Chaos",
            "Crispy",
        ]

    def load_pet_data(self):
        """Loads pet data from the JSON file."""
        if not os.path.exists(PET_DATA_FILE):
            return {"users": {}, "server_pet": {"name": "Guardian", "level": 1, "species": "Phoenix"}}
        with open(PET_DATA_FILE, "r") as file:
            return json.load(file)

    async def save_pet_data(self):
        """Safely writes pet data to the JSON file using a lock."""
        async with self.lock:  # Ensures only one process writes at a time
            with open(PET_DATA_FILE, "w") as file:
                json.dump(self.pets, file, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Pets Cog has loaded!')
    
    @staticmethod
    def time_since(timestamp):
        """Converts a timestamp string into 'X Hours Y Minutes Ago' format."""
        last_played_time = dt.datetime.fromisoformat(timestamp)  # Convert string to datetime
        now = dt.datetime.now()  # Current time
        diff = now - last_played_time  # Time difference

        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if diff.days > 0:
            return f"{diff.days} Days {hours} Hours Ago"
        elif hours > 0:
            return f"{hours} Hours {minutes} Minutes Ago"
        else:
            return f"{minutes} Minutes Ago"
    
    @commands.command(name='adopt')
    async def adopt(self, ctx):
        user_id = str(ctx.author.id)
        
        if user_id in self.pets["users"]:
            await ctx.send("You already have a pet!")
            return
        
        pet = random.choice(self.pet_list)
        pet_type = random.choice(self.type_list)

        # Default pet
        self.pets["users"][user_id] = {
            "name": "Unnamed",
            "species": pet,
            "type": pet_type,
            "age": "Baby",
            "exp": 0,
            "hunger": 100,
            "happiness": 100,
            "last_fed": str(dt.datetime.now()),
            "last_played": str(dt.datetime.now())
        }
        await self.save_pet_data()  # Use async function

        await ctx.send(f"{ctx.author.mention}, you have adopted a {pet}! 🐉 Give them a name with `!name <name>`")
        print(f"[{dt.datetime.now()}] {ctx.author} has adopted a {pet}!")

    @commands.command(name='name')
    async def name_pet(self, ctx, *, name: str):
        user_id = str(ctx.author.id)

        if user_id not in self.pets["users"]:
            await ctx.send("You don't have a pet yet! Use `!adopt` first.")
            return

        self.pets["users"][user_id]["name"] = name
        await self.save_pet_data()  # Use async function

        await ctx.send(f"Your pet is now named **{name}**! 🐾")

    @commands.command(name='feed')
    async def feed(self, ctx):
        '''Feed your pet to increase hunger percentage.'''
        user_id = str(ctx.author.id)

        if user_id not in self.pets["users"]:
            await ctx.send("You don't have a pet yet! Use `!adopt` first.")
            return
        

    @commands.command(name='view_pet')
    async def pet(self, ctx):
        user_id = str(ctx.author.id)
        # load pet data
        if user_id not in self.pets["users"]:
            await ctx.send("You don't have a pet yet! Use `!adopt` first.")
            return
        
        pet = self.pets["users"][user_id]
        pet_name = pet["name"]
        pet_species = pet["species"]
        pet_level = pet["level"]
        pet_type = pet["type"]
        pet_age = pet["age"]
        pet_hunger = pet["hunger"]
        pet_happiness = pet["happiness"]
        pet_last_fed = pet["last_fed"]
        pet_last_played = pet["last_played"]

        await ctx.send(f"```{pet_name} the {pet_species} ({pet_type})\n"
                       f"Level: {pet_level}\n"
                       f"Age: {pet_age}\n"
                       f"Hunger: {pet_hunger}%\n"
                       f"Happiness: {pet_happiness}%\n"
                       f"Last fed: {self.time_since(pet_last_fed)}\n"
                       f"Last played: {self.time_since(pet_last_played)}```")

async def setup(bot):
    await bot.add_cog(PetsCog(bot))

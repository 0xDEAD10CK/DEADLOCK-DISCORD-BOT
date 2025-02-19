import discord
from discord.ext import commands
import random
import os

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel = os.getenv('WELCOME_CHANNEL_ID')
        self.welcome_messages = [
            "Welcome, {user}! We were expecting you… Just kidding, but glad you're here!",
            "Hey {user}, welcome to the chaos! Grab a snack and brace yourself.",
            "Oh no, it's {user}! Just kidding, welcome aboard!",
            "A wild {user} appeared! Quick, throw a Pokéball!",
            "Welcome {user}! We have memes, madness, and occasionally meaningful conversations.",
            "Ahoy, {user}! Set sail for adventure and questionable decisions.",
            "Greetings, {user}! Your presence has increased the server’s coolness by 10%.",
            "Welcome {user}! We checked, and you don’t owe us money. Yet.",
            "Ding ding! {user} has entered the arena!",
            "Hello {user}! You're now legally obligated to post at least one meme.",
            "Welcome {user}! Hope you brought pizza… No? Okay, fine, you can stay.",
            "Hey {user}, we just started a bet on how long you’ll stay. Don’t disappoint us.",
            "Welcome, {user}! Don’t worry, we don’t bite. Well… most of us don’t.",
            "Look who's here! It's {user}! Everyone act normal.",
            "Welcome, {user}! You broke the server… Just kidding, but that would have been funny.",
            "Brace yourself, {user} has arrived!",
            "New player {user} has joined the game!",
            "Welcome {user}! May your memes be dank and your WiFi stable.",
            "Welcome {user}! If you find the secret entrance, let us know. We lost it.",
            "Oh great, another human! Welcome, {user}! Or are you a bot? Blink twice if not.",
            "Welcome {user}! Please read the rules. Or don’t. I’m not your mom.",
            "Hey {user}, your probation period starts now. Just kidding… or am I?",
            "Welcome {user}! You just unlocked the ‘Joined a Discord Server’ achievement!",
            "Watch out, everyone! {user} has arrived and is ready to cause trouble!",
            "Welcome, {user}! Don't ask about the last guy... we don't talk about him.",
            "Welcome, {user}! You just made this server 87% cooler!",
            "Welcome {user}! We hope you like terrible jokes, because we have a lot of them.",
            "What’s up, {user}? You’ve entered a realm of madness. Enjoy your stay!",
            "We got a fresh one! Welcome, {user}, to the land of the weird!",
            "Welcome {user}! We just sacrificed a bot to bring you here. Worth it.",
            "Attention everyone! {user} has entered the building! Sound the alarms!",
            "You thought you could just join and not be noticed? Ha! Welcome, {user}!",
            "Welcome, {user}! The prophecy foretold your arrival… kind of.",
            "Welcome {user}! Your presence has been logged and your data sold. Just kidding… maybe.",
            "Welcome {user}! You have been chosen. For what? No idea, but congrats!",
            "Halt! Who goes there? Oh, it’s just {user}. Carry on.",
            "Welcome {user}! Your initiation ritual begins… now! Just kidding. Or am I?",
            "Look at that, {user} just dropped in! We’re doomed—I mean, welcome!",
            "Welcome, {user}! We have cookies. Okay, not really, but we wish we did.",
            "Welcome {user}! By joining, you agree to our unwritten rules. Too bad we lost them.",
            "It’s a bird! It’s a plane! No, wait… it’s {user}! Welcome!",
            "Welcome {user}! No refunds, no take-backs, and absolutely no escape.",
            "Welcome, {user}! You’re now part of this weird, wonderful family. Good luck!",
            "Welcome, {user}! Try not to trip over the chaos on your way in.",
            "Behold! A new challenger approaches! Welcome, {user}!",
            "Welcome {user}! You are now legally required to laugh at our bad jokes.",
            "Welcome {user}! If you hear screams in the distance, don’t worry. That’s normal.",
            "Hey {user}, welcome! You have been automatically assigned 100 cool points!",
            "Welcome {user}! You’re just in time for absolutely nothing scheduled.",
            "Welcome {user}! You’ve joined the best server. Or at least, the one you clicked on."
        ]


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

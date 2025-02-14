import discord
from discord.ext import commands
import datetime as dt

class RainbowCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.RAINBOW_ANSI_CODES = [
            "\033[1;31m",  # Bright Red
            "\033[1;33m",  # Bright Yellow
            "\033[1;32m",  # Bright Green
            "\033[1;36m",  # Bright Cyan
            "\033[1;34m",  # Bright Blue
            "\033[1;35m",  # Bright Magenta
            "\033[2;31m",  # Dim Red
            "\033[2;33m",  # Dim Yellow
            "\033[2;32m",  # Dim Green
            "\033[2;36m",  # Dim Cyan
            "\033[2;34m",  # Dim Blue
            "\033[2;35m",  # Dim Magenta
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ WORKING ] - Rainbow Message Cog has loaded!')

    @commands.command(name='rainbow')
    async def rainbow_message(self, ctx, *, message: str):
        """
        Sends a rainbow-colored message using ANSI codes.
        """
        if not message:
            await ctx.send("Please provide a message to rainbowify!")
            return

        rainbow_message = ""
        for i, char in enumerate(message):
            color = self.RAINBOW_ANSI_CODES[i % len(self.RAINBOW_ANSI_CODES)]
            rainbow_message += f"{color}{char}"

        # Reset color at the end
        rainbow_message += "\033[0m"

        print(f'[{dt.datetime.now()}] {ctx.author} has generated Rainbow Text!')
        await ctx.send(f"```ansi\n{rainbow_message}\n```")

async def setup(bot):
    await bot.add_cog(RainbowCog(bot))

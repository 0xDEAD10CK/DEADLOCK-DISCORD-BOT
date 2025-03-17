import discord
from discord.ext import commands
import yt_dlp
import asyncio
import datetime
from collections import deque

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_queue = deque()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[ CURRENTLY BROKEN] - Music Cog has loaded!')

    @commands.command(name='play')
    async def play(self, ctx, *, url):
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()

        self.audio_queue.append(url)
        if not ctx.voice_client.is_playing():
            await self.stream_audio_to_discord(ctx.voice_client)

    async def stream_audio_to_discord(self, vc):
        while self.audio_queue:
            url = self.audio_queue.popleft()
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'default_search': 'ytsearch',
                'noplaylist': True,
                'extract_flat': False
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    audio_url = info_dict['url']

                ffmpeg_options = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }

                vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: print(f'Finished playing: {e}'))
                while vc.is_playing():
                    await asyncio.sleep(1)
            except Exception as e:
                print(f'Error streaming audio: {e}')

                filename = f'music_error_log_{datetime.datetime.now}.txt'
                with open(filename, 'w') as f:
                    f.write(f'Error streaming audio: {e}')
                    f.close()
                await vc.disconnect()

async def setup(bot):
    await bot.add_cog(MusicCog(bot))
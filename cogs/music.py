import discord
from discord.ext import commands
import asyncio
import yt_dlp


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {}
        self.voice_clients = {}
        self.rutube_base_url = 'https://rutube.ru/'
        self.rutube_watch_url = self.rutube_base_url + 'video/'

    @commands.command(name="play")
    async def play(self, ctx, *, link):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You need to be in a voice channel to play music.")
            return

        try:
            voice_client = await ctx.author.voice.channel.connect()
            self.voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            await ctx.send(f"Error connecting to voice channel: {e}")
            return

        try:
            if "rutube.ru" not in link:
                video_id = link.split('/')[-1]
                link = self.rutube_watch_url + video_id

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL({}).extract_info(
                    link,
                    download=False
                )
            )

            song = data['url']

            self.voice_clients[ctx.guild.id].play(
                discord.FFmpegOpusAudio(song, executable="ffmpeg", options="-vn"),
                after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.client.loop)
            )
            await ctx.send(f"Now playing: {link}")
        except Exception as e:
            await ctx.send(f"Error playing song: {e}")

    async def play_next(self, ctx):
        if ctx.guild.id in self.queues and self.queues[ctx.guild.id]:
            link = self.queues[ctx.guild.id].pop(0)
            await self.play(ctx, link=link)

    @commands.command(name="clear_queue")
    async def clear_queue(self, ctx):
        if ctx.guild.id in self.queues:
            self.queues[ctx.guild.id].clear()
            await ctx.send("Queue cleared!")
        else:
            await ctx.send("There is no queue to clear")

    @commands.command(name="pause")
    async def pause(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].pause()
            await ctx.send("Playback paused")
        except Exception as e:
            await ctx.send(f"Error pausing: {e}")

    @commands.command(name="resume")
    async def resume(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].resume()
            await ctx.send("Your playback resumed")
        except Exception as e:
            await ctx.send(f"Error resuming the playback: {e}")

    @commands.command(name="stop")
    async def stop(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.voice_clients[ctx.guild.id].disconnect()
            del self.voice_clients[ctx.guild.id]
            await self.play_next(ctx)
            await ctx.send("Your playback stopped")
        except Exception as e:
            await ctx.send(f"Error while stopping: {e}")

    @commands.command(name="queue")
    async def queue(self, ctx, *, url):
        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
        self.queues[ctx.guild.id].append(url)
        await ctx.send("Added to queue!")


async def setup(client):
    await client.add_cog(Music(client))

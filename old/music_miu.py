# import os
# import discord
# from discord.ext import commands
# import asyncio
# import yt_dlp
# from dotenv import load_dotenv
# import logging.handlers
#
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# logging.getLogger('discord.http').setLevel(logging.INFO)
#
# handler = logging.handlers.RotatingFileHandler(
#     filename='discord.log',
#     encoding='utf-8',
#     maxBytes=32 * 1024 * 1024,
#     backupCount=5,
# )
# dt_fmt = '%Y-%m-%d %H:%M:%S'
# formatter = logging.Formatter(
#     '[{asctime}] [{levelname:<8}] {name}: {message}',
#     dt_fmt,
#     style='{'
# )
# handler.setFormatter(formatter)
# logger.addHandler(handler)
#
# load_dotenv()
# discord_token = os.getenv('DISCORD_TOKEN')
#
# if discord_token is None:
#     print("Error: DISCORD_TOKEN environment variable is not set or deleted.")
#     exit(1)
#
# intents = discord.Intents.default()
# intents.message_content = True
#
# rutube_base_url = 'https://rutube.ru/'
# rutube_watch_url = rutube_base_url + 'video/'
#
# client = commands.Bot(
#     command_prefix="$",  # /play
#     intents=intents
# )
# queues = {}
# voice_clients = {}
#
#
# @client.event
# async def on_ready():
#     print(f'{client.user} is now singing songs, ~meow :3')
#
#
# @client.command(name="play")
# async def play(ctx, *, link):
#     if ctx.author.voice is None or ctx.author.voice.channel is None:
#         await ctx.send("You need to be in a voice channel to play music.")
#         return
#
#     try:
#         voice_client = await ctx.author.voice.channel.connect()
#         voice_clients[voice_client.guild.id] = voice_client
#     except Exception as e:
#         print(e)
#
#     try:
#         if "rutube.ru" not in link:
#             video_id = link.split('/')[-1]
#             link = rutube_watch_url + video_id
#
#         loop = asyncio.get_event_loop()
#         data = await loop.run_in_executor(
#             None,
#             lambda: yt_dlp.YoutubeDL({}).extract_info(
#                 link,
#                 download=False
#             )
#         )
#
#         song = data['url']
#
#         voice_clients[ctx.guild.id].play(
#             discord.FFmpegOpusAudio(song, executable="ffmpeg.exe", options="-vn"),
#             after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop)
#         )
#     except Exception as e:
#         print(e)
#
#
# async def play_next(ctx):
#     if ctx.guild.id in queues and queues[ctx.guild.id]:
#         link = queues[ctx.guild.id].pop(0)
#         await play(ctx, link=link)
#
#
# @client.command(name="clear_queue")
# async def clear_queue(ctx):
#     if ctx.guild.id in queues:
#         queues[ctx.guild.id].clear()
#         await ctx.send("Queue cleared!")
#     else:
#         await ctx.send("There is no queue to clear")
#
#
# @client.command(name="pause")
# async def pause(ctx):
#     try:
#         voice_clients[ctx.guild.id].pause()
#     except Exception as e:
#         print(e)
#
#
# @client.command(name="resume")
# async def resume(ctx):
#     try:
#         voice_clients[ctx.guild.id].resume()
#     except Exception as e:
#         print(e)
#
#
# @client.command(name="stop")
# async def stop(ctx):
#     try:
#         voice_clients[ctx.guild.id].stop()
#         await voice_clients[ctx.guild.id].disconnect()
#         del voice_clients[ctx.guild.id]
#         await play_next(ctx)
#     except Exception as e:
#         print(e)
#
#
# @client.command(name="queue")
# async def queue(ctx, *, url):
#     if ctx.guild.id not in queues:
#         queues[ctx.guild.id] = []
#     queues[ctx.guild.id].append(url)
#     await ctx.send("Added to queue!")
#
#
# client.run(discord_token)

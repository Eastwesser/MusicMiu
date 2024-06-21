import os
import discord
from discord.ext import commands
from utils.env_loader import load_env
from utils.logging_config import configure_logging

configure_logging()

load_env()

discord_token = os.getenv('DISCORD_TOKEN')

if discord_token is None:
    print("Error: DISCORD_TOKEN environment variable is not set or deleted.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is now singing songs, ~meow :3')


async def load_extensions():
    cogs = ['cogs.music']
    for cog in cogs:
        await client.load_extension(cog)


async def main():
    async with client:
        await load_extensions()
        await client.start(discord_token)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

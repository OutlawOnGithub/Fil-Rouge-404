# main.py
import discord
from discord.ext import commands
import json
import os

async def main():
    # Load token from environment or config

    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents.all()
    bot = commands.Bot(
        command_prefix="!",
        intents=intents,
        activity=discord.Activity(type=discord.ActivityType.playing, name="!help"),
        help_command=None
    )

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    # Automatically load all cogs from the cogs folder
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"Loaded cog: {file}")
            except Exception as e:
                print(f"Failed to load cog {file}: {e}")

    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    
    
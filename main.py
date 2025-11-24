import discord
from discord.ext import commands, tasks
import os
from datetime import datetime, timezone
import asyncio




async def main():
    TOKEN = os.getenv("DISCORD_TOKEN")
    DB_PW = os.getenv("POSTGRES_PASSWORD")
    PREFIX = os.getenv("BOT_PREFIX")
    SCHEME = os.getenv("SCHEME")


    bot = commands.Bot(
        command_prefix=PREFIX,
        intents=discord.Intents.all(),
        activity=discord.Activity(type=discord.ActivityType.playing, name=PREFIX+"help"),
        help_command=None,
    )   

    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")

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
    
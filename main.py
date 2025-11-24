import discord
from discord.ext import commands
import os
import asyncio
from utils.db import Database  # le fichier db.py créé précédemment

async def main():
    TOKEN = os.getenv("DISCORD_TOKEN")
    DB_PW = os.getenv("POSTGRES_PASSWORD")
    PREFIX = os.getenv("BOT_PREFIX", "!")  # valeur par défaut
    SCHEME = os.getenv("SCHEME", "postgresql")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_NAME = os.getenv("POSTGRES_DB", "mydb")

    # DSN pour asyncpg
    DSN = f"{SCHEME}://{DB_USER}:{DB_PW}@{DB_HOST}:5432/{DB_NAME}"

    # Crée le bot
    bot = commands.Bot(
        command_prefix=PREFIX,
        intents=discord.Intents.all(),
        activity=discord.Activity(type=discord.ActivityType.playing, name=PREFIX + "help"),
        help_command=None,
    )

    # -----------------------------
    # Connexion à la base de données
    # -----------------------------
    bot.db = Database(dsn=DSN)
    await bot.db.connect()
    print("✅ Database connected!")

    # -----------------------------
    # Event on_ready
    # -----------------------------
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} | ID: {bot.user.id}")

    # -----------------------------
    # Charger automatiquement tous les Cogs
    # -----------------------------
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                # On passe la DB à chaque cog
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"✅ Loaded cog: {file}")
            except Exception as e:
                print(f"❌ Failed to load cog {file}: {e}")

    # -----------------------------
    # Démarrer le bot
    # -----------------------------
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())

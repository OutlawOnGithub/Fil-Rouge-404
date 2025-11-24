import discord
from discord.ext import commands
import asyncpg
import random
import logging
import os

# --------------------------
# Configure logging
# --------------------------
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)  # Normal log level
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# --------------------------
# Cog
# --------------------------
class Base(commands.Cog):
    def __init__(self, bot, db_pw: str):
        self.bot = bot
        self.db_pw = db_pw
        self.db_host = "postgres_fl"  # Docker container name
        self.db_name = "filrouge"
        self.db_user = "filrouge"
        self.db_port = 5432
        self.pool = None

    async def connect_db(self):
        """Try to connect to PostgreSQL and create a connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                user=self.db_user,
                password=self.db_pw,
                database=self.db_name,
                host=self.db_host,
                port=self.db_port,
                min_size=1,
                max_size=5
            )
            logger.info("✅ Successfully connected to the database.")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to DB: {e}")
            return False

    # ----------------------------
    # Commands
    # ----------------------------
    @commands.command(name="quoi")
    async def quoi(self, ctx):
        await ctx.send("feur")

    @commands.command(name="beurre")
    async def beurre(self, ctx):
        await ctx.send(f"Tu as gagné {random.randint(0,10)} beurres !")

    @commands.command(name="pull")
    async def pull(self, ctx):
        """Check DB connection first"""
        if self.pool is None:
            success = await self.connect_db()
            if not success:
                await ctx.send("❌ Failed to connect to the database!")
                return
            else:
                await ctx.send("✅ Successfully connected to the database!")

        # Example logic: roll between 0-10
        roll = random.randint(0, 10)
        await ctx.send(f"🎰 Pull result: {roll} beurres lost/won!")

# ----------------------------
# Setup function
# ----------------------------
async def setup(bot):
    db_pw = os.getenv("POSTGRES_PASSWORD")
    await bot.add_cog(Base(bot, db_pw))

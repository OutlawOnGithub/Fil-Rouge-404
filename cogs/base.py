import discord
import psycopg2
from discord.ext import commands
import random
from utils.embeds import CustomEmbed

class Base(commands.Cog):
    def __init__(self, bot, DB_PW):
        self.bot = bot
        conn = psycopg2.connect(
            dbname="filrouge",
            user="filrouge",
            password=DB_PW,
            host="postgres_fl",  # This is the name of the PostgreSQL container
            port="5432"  # Default PostgreSQL port
        )

    @commands.command(name="quoi")
    async def quoi(self, ctx, *args):
        await ctx.send(f"feur")

    @commands.command(name="beurre")
    async def beurre(self, ctx, *args):
        await ctx.send(f"Tu as gagné {random.randint(0, 10)} beurres !")

    @commands.command(name="pull")
    async def pull(self, ctx, *args):
        player = ctx.user
        await ctx.send(f"Tu as gagné {random.randint(0, 10)} beurres !")

        

# Fonction setup pour Discord.py v2
async def setup(bot):
    await bot.add_cog(Base(bot))
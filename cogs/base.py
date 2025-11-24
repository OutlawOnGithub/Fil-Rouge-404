import discord
from discord.ext import commands
import random

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quoi")
    async def roll(self, ctx, *args):
        await ctx.send(f"feur")

# Fonction setup pour Discord.py v2
async def setup(bot):
    await bot.add_cog(Base(bot))
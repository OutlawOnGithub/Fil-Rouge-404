import discord
from discord.ext import commands
import random
from utils.embeds import CustomEmbed

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quoi")
    async def roll(self, ctx, *args):
        await ctx.send(f"feur")

    @commands.command(name="pull")
    async def roll(self, ctx, *args):
        await ctx.send(f"Tu as gagné {random.randint(0, 10)} beurres !")

# Fonction setup pour Discord.py v2
async def setup(bot):
    await bot.add_cog(Base(bot))
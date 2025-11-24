import discord
from discord.ext import commands
import random

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quoi")
    async def roll(self, ctx, *args):
        await ctx.send(f"feur")
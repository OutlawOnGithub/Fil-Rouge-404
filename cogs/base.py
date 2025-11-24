import discord
from discord.ext import commands
import random
import time

from utils.embeds import CustomEmbed  # Si tu veux l'utiliser
from utils.db import Database

class Base(commands.Cog):
    def __init__(self, bot, db: Database):
        self.bot = bot
        self.db = db
        self.PULL_COST = 5

    # --------------------------
    #  Commandes simples
    # --------------------------
    @commands.command(name="quoi")
    async def quoi(self, ctx, *args):
        await ctx.send("feur")

    @commands.command(name="beurre")
    async def beurre(self, ctx, *args):
        await ctx.send(f"Tu as gagné {random.randint(0, 10)} beurres !")

    # --------------------------
    #     Commande PULL
    # --------------------------
    @commands.command(name="pull")
    async def pull(self, ctx, *args):
        user_id = ctx.author.id
        timestamp = int(time.time())

        # S'assure que l'utilisateur existe
        await self.db.add_user_if_not_exists(user_id)
        user = await self.db.get_user(user_id)

        # Vérifie le solde
        if user['balance'] < self.PULL_COST:
            await ctx.send(f"❌ Tu n'as pas assez de beurres ! Il te faut **{self.PULL_COST}**.")
            return

        # Retire le coût
        await self.db.update_balance(user_id, -self.PULL_COST)

        # Roll 0-100
        roll = random.randint(0, 100)
        if roll < 80:
            result = "💩 **CACA**"
        elif roll < 100:
            result = "😐 **BOF**"
        else:
            result = "🐐 **GOAT**"
            # Exemple: on ajoute un objet rare
            await self.db.add_object(user_id, "Goat Trophy")

        # Met à jour lastPull
        await self.db.update_last_pull(user_id, timestamp)

        await ctx.send(f"🎰 Résultat du pull : **{roll}** → {result}")

# --------------------------
# Setup Cog
# --------------------------
async def setup(bot):
    # Création DB
    db = Database(dsn="postgresql://user:password@localhost:5432/postgres")
    await db.connect()

    await bot.add_cog(Base(bot, db))

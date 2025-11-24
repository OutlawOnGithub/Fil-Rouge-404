import os
import discord
from discord.ext import commands
from database import Database
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord')

# Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')
SCHEME = os.getenv('SCHEME', 'filrouge')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

print(f"=== Configuration ===")
print(f"PREFIX: '{PREFIX}'")
print(f"SCHEME: '{SCHEME}'")
print(f"TOKEN configuré: {'Oui' if TOKEN else 'Non'}")
print(f"=====================")

# Database connection
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'filrouge',
    'user': 'filrouge',
    'password': POSTGRES_PASSWORD,
    'schema': SCHEME
}

# Bot setup avec tous les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
db = Database(DB_CONFIG)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} est connecté et prêt!')
    print(f'✅ Prefix: "{PREFIX}"')
    print(f'✅ Guilds: {len(bot.guilds)}')
    await db.connect()

@bot.event
async def on_message(message):
    print(f"📨 Message reçu: '{message.content}' de {message.author}")
    print(f"   Commence par prefix? {message.content.startswith(PREFIX)}")
    await bot.process_commands(message)

@bot.command(name='quoi')
async def quoi(ctx):
    """Répond 'feur' à la commande !quoi"""
    print(f"🎯 Commande 'quoi' exécutée par {ctx.author}")
    await ctx.send('feur')

@bot.command(name='beurre')
async def beurre(ctx):
    """Tire entre 2 et 20 beurres et l'ajoute à la balance du joueur"""
    print(f"🎯 Commande 'beurre' exécutée par {ctx.author}")
    user_id = ctx.author.id
    amount = await db.add_beurre(user_id)
    balance = await db.get_balance(user_id)
    
    await ctx.send(f'{ctx.author.mention} a gagné **{amount} beurre(s)** ! 🧈\nBalance totale : **{balance} beurre(s)**')

@bot.command(name='pull')
async def pull(ctx):
    """Utilise la balance pour tirer un objet au sort"""
    print(f"🎯 Commande 'pull' exécutée par {ctx.author}")
    user_id = ctx.author.id
    result = await db.pull_object(user_id)
    
    if result['error']:
        await ctx.send(f"{ctx.author.mention} {result['message']}")
    else:
        emoji_map = {
            'bout de bois': '🪵',
            'crotte': '💩',
            'lingot': '🏆'
        }
        emoji = emoji_map.get(result['object'], '❓')
        
        await ctx.send(
            f"{ctx.author.mention} a dépensé **{result['cost']} beurre(s)** et a obtenu : **{result['object']}** {emoji}\n"
            f"Balance restante : **{result['new_balance']} beurre(s)**"
        )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f'Erreur : {error}')

if __name__ == '__main__':
    bot.run(TOKEN)
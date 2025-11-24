import discord

class CustomEmbed:

    def __init__(self, color: discord.Color, title: str, content):
        embed = discord.Embed
        embed.color = color
        embed.title = title
        embed.fields = content

        embed.footer = "ceci est le footer"
import discord

class CustomEmbed(discord.Embed):
    
    def __init__(self, color, title, content):
        super().__init__(title=title, color=color, description=content)
        self.set_footer(text="ceci est le footer")
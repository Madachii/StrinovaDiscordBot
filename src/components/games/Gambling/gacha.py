import discord
from components.component import Component
from components.games.Gambling.strinovabanner import Banner
from discord.ext import commands

class Gacha(commands.Cog, Component):
    def __init__(self, bot, db = None):
        self.bot = bot
        self.banners = []

    def load_banner(self, banner: Banner):
        self.banners.append(banner)
        
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f'Hello {member.name}~')
        
    @commands.command()
    async def pull(self, ctx, *, member: discord.Member = None):
        await ctx.send("Pulled")
        pass
        
        
    def help(self):
        # Implement the help method here, as Component's help is abstract
        return "This is the help for the Gacha class"
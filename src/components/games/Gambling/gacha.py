import discord
import discord.ext.commands
import secrets
import bisect
from components.component import Component
from components.games.gambling.strinovabanner import Banner
from discord.ext import commands
from db.GachaDb import GachaDb
import discord.ext

class Gacha(commands.Cog, Component):
    DEFAULT_PROBABILITY = (0.0065, 0.05, 0.24, 0.7035)
    RARITY_MAPPING = {0: "Legendary", 1: "Epic", 2: "Rare", 3: "Refined"}
    COLOR_MAPPING = {"Legendary": "#F85555", "Epic": "#FFC555", "Rare": "#F285FF", "Refined": "#60A3F7"}
    PULL_PRICE = 120

    def __init__(self, bot, db: GachaDb):
        self.bot = bot
        self.db = db
        self.banners = []

    def load_banner(self, banner_name: str):
        banner = Banner(self.db, banner_name, Gacha.DEFAULT_PROBABILITY)
        self.banners.append(banner)
        
    @commands.command()
    async def bablo(self, ctx: discord.ext.commands.context.Context):
        user_bablo = await self.db.get_bablo(ctx.author.id)
        if (not user_bablo):
            await ctx.send("You don't have enough bablo")
            return
        
        await ctx.send(f"You have {user_bablo[0][0]} bablos!") # TODO: could probably use the bablo emoji to make it look better
        
    @commands.command()
    async def inv(self, ctx: discord.ext.commands.context.Context):
        result = await self.db.get_inv(ctx.author.id, "Mecha_Angel")
        print(result)
        
    @commands.command()
    async def pull(self, ctx: discord.ext.commands.context.Context):
        if (len(self.banners) <= 0):
            await ctx.send("There are no active banners at this time!")
            return
    
        data = await self.db.get_user_data(ctx.author.id, "bablo", "active_banner")
        user_bablo, user_banner = data[0]
        if (not user_bablo or not user_banner):
            await ctx.send("Internal error bwah")
            return
        
        if (user_bablo < Gacha.PULL_PRICE):
            await ctx.send("You don't have enough bablo")
            return
        
        banner: Banner = self.banners[user_banner] # TODO: check what banner the user has currently, else set it to the default one [the newest]

        user_drop = await banner.pull() 
        
        await self.db.subtract_bablo(ctx.author.id, Gacha.PULL_PRICE)
        await self.db.add_drop(ctx.author.id, user_drop[0])
       
        embed: discord.Embed = discord.Embed()
        embed.title = user_drop[1]
        embed.colour = discord.Colour.from_str(Gacha.COLOR_MAPPING[user_drop[2]])
        embed.set_image(url=user_drop[3])
        embed.set_footer(text=f"You still have {user_bablo - 120} bablo left!")

        await ctx.send(embed=embed)
        
    @commands.command()
    async def debug(self, ctx: discord.ext.commands.context.Context, amount: int):
        id = ctx.author.id
        await self.db.add_bablo(id, amount)
            
        await ctx.send(f"Increased {ctx.author.name} bablo by {amount}!")
    
    def help(self):
        # Implement the help method here, as Component's help is abstract
        return "This is the help for the Gacha class"
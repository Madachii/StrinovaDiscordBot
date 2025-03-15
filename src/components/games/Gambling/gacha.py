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
    rarity_mapping = {0: "Legendary", 1: "Epic", 2: "Rare", 3: "Refined"}

    def __init__(self, bot, db: GachaDb):
        self.bot = bot
        self.banners = []
        self.db = db

    def load_banner(self, banner: Banner):
        self.banners.append(banner)
        
    @commands.command()
    async def hello(self, ctx: discord.ext.commands.context.Context):
        member = member or ctx.author
        await ctx.send(f'Hello {member.name}~')
        
    @commands.command()
    async def pull(self, ctx: discord.ext.commands.context.Context):
        if (len(self.banners) <= 0):
            await ctx.send("There are no active banners at this time!")
            return
        
        banner: Banner = self.banners[0] # TODO: check what banner the user has currently, else set it to the default one [the newest]

        rng = secrets.SystemRandom().randrange(0, banner.weights[-1])
        idx = bisect.bisect_right(banner.weights, rng)

        result = await self.db.get_banner_drops("Mecha_Angel", Gacha.rarity_mapping[idx])
        user_drop = result[rng % len(result)] 
       
        print(len(result)) 
        print(rng)
        await ctx.send(f"{ctx.author.name} just got: {str(user_drop)}")
            
        
        # drop = None
        # if rng >= 0 and rng < weights[0]:
        #     rng = secrets.SystemRandom().randrange(0, len(banner.pool["Legendary"])) # TODO: Could take the modulo o the previous rng number and limit it between 0 - n where n is the drops
        #     drop = banner.pool["Legendary"][rng]
        # elif rng >= weights[0] and rng < weights[1]:
        #     rng = secrets.SystemRandom().randrange(0, len(banner.pool["Epic"]))
        #     drop = banner.pool["Epic"][rng]
        # elif rng >= weights[1] and rng < weights[2]:
        #     rng = secrets.SystemRandom().randrange(0, len(banner.pool["Rare"]))
        #     drop = banner.pool["Rare"][rng]
        # elif rng >= weights[2] and rng < weights[3]:
        #     rng = secrets.SystemRandom().randrange(0, len(banner.pool["Refined"]))
        #     drop = banner.pool["Refined"][rng]

        # if (drop != None):
        #     print("You got: " + drop.name)
        # else:
        #     print("HUH")
        
    @commands.command()
    async def debug(self, ctx: discord.ext.commands.context.Context):
        await self.db.add_user(ctx.author.id)
        
        result = await self.db.get_user(ctx.author.id)
        
        print("Got: ", str(result))
        
        if result is not None:
            await ctx.send(f"{ctx.author.id} has {result[0][1]} babloons")
        pass
    def help(self):
        # Implement the help method here, as Component's help is abstract
        return "This is the help for the Gacha class"
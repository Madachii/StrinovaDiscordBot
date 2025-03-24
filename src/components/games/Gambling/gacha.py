import discord
import discord.ext.commands
import secrets
import bisect
import asyncio
from components.component import Component
from components.games.gambling.strinovabanner import Banner
from discord.ext import commands
from db.GachaDb import GachaDb
import discord.ext

class Gacha(commands.Cog, Component):
    DEFAULT_PROBABILITY = (0.0065, 0.05, 0.24, 0.7035)
    RARITY_MAPPING = {0: "Legendary", 1: "Epic", 2: "Rare", 3: "Refined"}
    COLOR_MAPPING = {"Legendary": "#F85555", "Epic": "#FFC555", "Rare": "#F285FF", "Refined": "#60A3F7"}
    EMOMTE_MAPPING = {"Legendary": "🟥", "Epic" : "🟨", "Rare": "🟪", "Refined": "🟦"}
    PULL_PRICE = 120

    def __init__(self, bot, db: GachaDb):
        self.bot = bot
        self.db = db
        self.banners = []

    def load_banner(self, uuid: str, banner_name: str):
        banner = Banner(uuid=uuid, db=self.db, title=banner_name, probabilities=Gacha.DEFAULT_PROBABILITY)
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
        try:
            result = await self.db.get_inv(ctx.author.id)
            if (not result):
                print("Failed to fetch")
                return
            
            user_bablo = result[0][1]
            embed: discord.Embed = discord.Embed()
            embed.title = f"{ctx.author.name} inventory"
             
            description = "\n".join(f"{self.EMOMTE_MAPPING[row[1]]} {row[0]}" for row in result) # TODO: add like a colored cube to represent rarity
            embed.set_footer(text=f"You have {user_bablo} babloons")
                
            embed.description = description
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        
    
    @commands.command()
    async def pull(self, ctx: discord.ext.commands.context.Context, times: int):
        try:
            if (len(self.banners) <= 0):
                await ctx.send("There are no active banners at this time!")
                return

            tasks = [self.__pull(ctx) for i in range(times)]
            result = await asyncio.gather(*tasks)
            print(result)

        except Exception as e:
            print(e)
        
    async def __pull(self, ctx: discord.ext.commands.context.Context):
        print(ctx.author.id)
        try:
            data = await self.db.get_user_data(ctx.author.id)
            if not data:
                print(f"Failed to get data for: {ctx.author.name}")
                return

            print(data)
            _, user_bablo, basestring,user_banner, legendary_pulls, epic_pulls, rare_pulls, weight_legendary, weight_epic, weight_rare, weight_refined = data[0]
            if (not user_bablo or not user_banner):
                await ctx.send("Internal error bwah")
                return
            
            if (user_bablo < Gacha.PULL_PRICE):
                await ctx.send("You don't have enough bablo")
                return
            
            banner = self.get_banner_from_uuid(user_banner)
            
            if (banner is None):
                print("Failed to find banner")
                return
            
            user_drop = None
            item_id = title = rarity = url = None
            difference = 0
            args = []

            if (legendary_pulls >= 80):
                user_drop = await banner.pull(self.cumulative_weights((100000, 0, 0, 0)))
                args, difference = await self.legendary_pull(weight_legendary, legendary_pulls=0, pity=True) # doesnt clear completly, need to change weight_legendary to db and fix it
                print("difference in legendary is: " + str(difference))
                    
            elif (epic_pulls >= 30):
                user_drop = await banner.pull(self.cumulative_weights((0,100000, 0, 0)))
                args, difference = await self.epic_pull(weight_epic, epic_pulls = 0, pity=True)

            elif (rare_pulls >= 10):
                user_drop = await banner.pull(self.cumulative_weights((0,0,100000, 0)))
                args, difference = await self.rare_pull(weight_rare, rare_pulls=0, pity=True)
                
            else:
                cumulative_weights = self.cumulative_weights((weight_legendary, weight_epic, weight_rare, weight_refined)) 
                user_drop = await banner.pull(cumulative_weights)
                
                _, _, rarity, _ = user_drop
                if rarity == "Legendary":
                    args, difference = await self.legendary_pull(weight_legendary, legendary_pulls = 0, pity=True)
                else:
                    extra_args, extra_difference = await self.legendary_pull(weight_legendary, legendary_pulls + 1, self.db.pity_bonus_legendary, pity=False)
                    difference += extra_difference
                    args.extend(extra_args)

                if rarity == "Epic":
                    args, difference = await self.epic_pull(weight_epic, epic_pulls = 0, pity=True)
                else:
                    extra_args, extra_difference = await self.epic_pull(weight_epic, epic_pulls + 1, self.db.pity_bonus_epic, pity=False)
                    args.extend(extra_args)
                    difference += extra_difference

                if rarity == "Rare":
                    args, difference = await self.rare_pull(weight_rare, rare_pulls=0, pity=True)
                else:
                    extra_args, extra_difference = await self.rare_pull(weight_rare, rare_pulls + 1, self.db.pity_bonus_rare, pity=False)
                    args.extend(extra_args)
                    difference += extra_difference

            args.append(('weight_refined', weight_refined - difference))
            args.append(('bablo', user_bablo - Gacha.PULL_PRICE))
            await self.db.update_user(ctx.author.id, args)

            item_id, title, rarity, url = user_drop 

            await self.db.add_drop(ctx.author.id, banner.uuid, item_id, rarity)

            embed = self.embed_pull_message(user_bablo, title, rarity, url)

            await ctx.send(embed=embed)

            return ((ctx.author.id, banner.uuid, item_id, rarity))
        except Exception as e:
            print(e)

    async def legendary_pull(self, weight_legendary = 0, legendary_pulls = 0, weight_pity = 0, pity = False):
        difference = 0
        args = []        
        if pity:
            args = [('weight_legendary', self.db.weight_legendary), ('legendary_pulls', 0)]
            difference += self.db.weight_legendary - weight_legendary
        else:
            args = [('weight_legendary', weight_legendary + weight_pity), ('legendary_pulls', legendary_pulls)]
            difference += self.db.pity_bonus_legendary
        
        return (args, difference)
    
    async def epic_pull(self, weight_epic, epic_pulls, weight_pity = 0, pity = False):
        difference = 0
        args = []        
        if pity:
            args = [('weight_epic', self.db.weight_epic), ('epic_pulls', 0)]
            difference += self.db.weight_epic - weight_epic 
        else:
            args = [('weight_epic', weight_epic + weight_pity), ('epic_pulls', epic_pulls)]
            difference += self.db.pity_bonus_epic

        return (args, difference)
        
    async def rare_pull(self, weight_rare, rare_pulls, weight_pity = 0, pity = False):
        difference = 0
        args = []        
        if pity:
            args = [('weight_rare', self.db.weight_rare), ('rare_pulls', 0)]
            difference += self.db.weight_rare - weight_rare 
        else:
            args = [('weight_rare', weight_rare + weight_pity), ('rare_pulls', rare_pulls)]
            difference += self.db.pity_bonus_rare

        return (args, difference)
    
    def cumulative_weights(self, weights):
        cumulative_weights = []
        add = 0
        for w in weights:
            add += w
            cumulative_weights.append(add)
        
        return cumulative_weights
    
    # this is fine for a small number of banners, even faster than a dictionary look up iirc
    def get_banner_from_uuid(self, uuid):
        for banner in self.banners:
            if (banner.uuid == uuid):
                return banner
        return None
    
    def embed_pull_message(self, user_bablo, title, rarity, url):
        embed: discord.Embed = discord.Embed()
        embed.title = title
        embed.colour = discord.Colour.from_str(Gacha.COLOR_MAPPING[rarity])
        embed.set_image(url=url)
        embed.set_footer(text=f"You still have {user_bablo - 120} bablo left!")

        return embed

    @commands.command()
    async def debug(self, ctx: discord.ext.commands.context.Context, amount: int):
        try:
            await self.db.add_user(ctx.author.id)
            await self.db.update_user(ctx.author.id, [("bablo", amount)])
            await ctx.send(f"Increased {ctx.author.name} bablo by {amount}!")

        except Exception as e:
            print(e)
    
    def help(self):
        # Implement the help method here, as Component's help is abstract
        return "This is the help for the Gacha class"
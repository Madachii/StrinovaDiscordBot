import discord
import discord.ext.commands
import asyncio
from components.component import Component
from components.games.gambling import BannerManager, GConstants
from components.games.gambling.user import User
from discord.ext import commands
from db.GachaDb import GachaDb
import discord.ext
import logging

class RollAgainButton(discord.ui.View):
    def __init__(self, gacha, ctx, times):
        super().__init__()
        self.gacha = gacha
        self.ctx = ctx
        self.times = times
        
        self.add_item(discord.ui.Button(label=f"You are going to pull {self.times} more times", style=discord.ButtonStyle.gray, disabled=True, row=2))

    @discord.ui.button(label="-5", style=discord.ButtonStyle.red)
    async def subtract_one(self, interaction: discord.Interaction, button: discord.ui.Button):

        self.times = max(1, self.times - 5)
        self.children[-1].label = self.pull_message(self.times)# make sure this is the You are going to ...

        await interaction.message.edit(view=self)
        await interaction.response.defer()
 
    @discord.ui.button(label=f"Pull Again", style=discord.ButtonStyle.primary)
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.gacha.pull(self.ctx, self.times)
        await interaction.response.defer()

    @discord.ui.button(label="+5", style=discord.ButtonStyle.green)
    async def add_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.times = min(10, (round(self.times / 5) * 5) + 5)
        self.children[-1].label = self.pull_message(self.times)
        
        await interaction.message.edit(view=self)
        await interaction.response.defer()
 
    
    def pull_message(self, times):
        return f"You are going to pull {times} more times"

class Gacha(commands.Cog, Component):
    def __init__(self, bot, db: GachaDb, logger: logging.Logger):
        self.bot = bot
        self.db = db
        self.logger = logger

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
             
            description = "\n".join(f"{GConstants.RARITY_MAPPING[row[1][1]]} {row[0]}" for row in result) # TODO: make this more clean later
            embed.set_footer(text=f"You have {user_bablo} babloons")
                
            embed.description = description
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        
    
    @commands.command()
    async def pull(self, ctx: discord.ext.commands.context.Context, times: int = 1):
        try:
            self.logger.info(f"Starting a {times} pull for {ctx.author.name}!")
            
            if BannerManager.is_empty():
                raise RuntimeError("There are no active banners at this time!")

            user: User = await User.get_user_data(ctx.author.id, self.db)
            
            print(user)
            
            data = await self.db.get_user_data(ctx.author.id)
            data = data[0]
            if not data:
                raise RuntimeError(f"Data for {ctx.author.name} is empty or invalid")

            # _, user_bablo, _, user_banner, _, _, _, _, _, _, _ = data[0]
            user_bablo, user_banner = (data[1], data[3])
            banner = BannerManager.get_banner_from_uuid(user_banner)
            if (banner is None):
                raise RuntimeError("Failed to find banner")
           
            final_price = GConstants.PULL_PRICE * times
            if (user_bablo < final_price):
               raise RuntimeError (f"You don't have enough bablo for: {times} pulls: {user_bablo} / {final_price}") 
            
            self.logger.info(f"Initial conditions passed for {ctx.author.name}!")
            
            loop_data = data
            drops = []
            for _ in range(times):
                loop_data = await banner.pull(ctx, loop_data, banner, drops)  

            # make this into a unpacking dict
            _, user_bablo, _, user_banner, legendary_pulls, epic_pulls, rare_pulls, weight_legendary, weight_epic, weight_rare, weight_refined = loop_data
            args = [
                ('bablo', user_bablo - final_price),
                ('weight_legendary', weight_legendary),
                ('weight_epic', weight_epic),
                ('weight_rare', weight_rare),
                ('weight_refined', weight_refined),
                ('legendary_pulls', legendary_pulls),
                ('epic_pulls', epic_pulls),
                ('rare_pulls', rare_pulls)
            ]
            await self.db.update_user(ctx.author.id, args)

            self.logger.info(f"Succcesfully updated {ctx.author.name} items with the new drops!")
            # transform add drop to use executemany instead
            tasks = [self.db.add_drop(ctx.author.id, user_banner, item_id, rarity) for item_id, _, rarity, _ in drops]
            return_val = await asyncio.gather(*tasks)

            embed = self.embed_pull_message(user_bablo - final_price, drops)
            
            view = RollAgainButton(self, ctx, times=times)
            
            await ctx.send(embed=embed, view=view, ephemeral=True)

        except Exception as e:
            print(e)
        
    def embed_pull_message(self, bablo, drops):
        _, itemName, mvp_rarity, mvp_url = drops[0]
        description = ""
        for drop in drops:
            itemID, itemName, rarity, url = drop

            current_emote, current_rank = GConstants.RARITY_MAPPING[rarity][1:]
            mvp_rank = GConstants.RARITY_MAPPING[mvp_rarity][2]

            if (current_rank <= mvp_rank):
                itemID, itemName, mvp_rarity, mvp_url = drop
                
            description += f"{current_emote} {itemName}\n"
        
        embed: discord.Embed = discord.Embed(description=description)
        embed.title = "The result of the pulls are..." 
        embed.colour = discord.Colour.from_str(GConstants.RARITY_MAPPING[mvp_rarity][0]) # TODO: make this cleaner later
        embed.set_image(url=mvp_url)
        embed.set_footer(text=f"You still have {bablo} bablo left!")

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
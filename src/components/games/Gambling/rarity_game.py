import discord
import discord.ext.commands
import asyncio
from components.component import Component
from components.games.gambling import Banner, BannerManager, GConstants
from discord.ext import commands
from db.GachaDb import GachaDb
import discord.ext
import logging


class Wager(discord.ui.View):
    def __init__(self, gacha, ctx, times):
        super().__init__()
        self.gacha = gacha
        self.ctx = ctx
        self.times = times

    @discord.ui.button(label="-100", style=discord.ButtonStyle.red)
    async def subtract_one(self, interaction: discord.Interaction, button: discord.ui.Button):

        self.times = max(1, self.times - 5)
        self.children[-1].label = self.pull_message(self.times)# make sure this is the You are going to ...

        await interaction.message.edit(view=self)
        await interaction.response.defer()
 
    @discord.ui.button(label=f"Pull Again", style=discord.ButtonStyle.primary)
    async def button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.gacha.pull(self.ctx, self.times)
        await interaction.response.defer()

    @discord.ui.button(label="+100", style=discord.ButtonStyle.green)
    async def add_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.times = min(10, (round(self.times / 5) * 5) + 5)
        self.children[-1].label = self.pull_message(self.times)
        
        await interaction.message.edit(view=self)
        await interaction.response.defer()
 
    
    def pull_message(self, times):
        return f"You are going to pull {times} more times"


class RarityGame(commands.Cog, Component):
    def __init__(self, bot, db: GachaDb, logger:logging.Logger):
        self.bot = bot
        self.db = db
        self.logger = logger
        
        self.legendary_mult = 20 
        self.epic_mult = 5
        self.rare_mult = 2
        self.refined_mult = 1
    
    @commands.command()
    async def play(self, ctx: discord.ext.commands.context.Context, legendary_bet: int, epic_bet: int, rare_bet: int, refined_bet: int):
        try:
            data = await self.db.get_user_data(ctx.author.id)
            if not data:
                raise RuntimeError(f"Data for {ctx.author.name} is empty or invalid")
            
            _, user_bablo, _, user_banner, _, _, _, _, _, _, _ = data[0]
            
            banner = BannerManager.get_banner_from_uuid(user_banner)
            if (banner is None):
                raise RuntimeError("Failed to find banner")
            
            drops = []
            tasks = [banner.pull(ctx, data[0], banner, drops) for _ in range(5)]
            result = await asyncio.gather(*tasks)

            count = {"Legendary" : 0, "Epic" : 0, "Rare" : 0, "Refined": 0}
            final_mult = 1
            for drop in drops:
                _, _, rarity, _ = drop
                count[rarity] += 1

            final_mult *= self.apply_multiplier(legendary_bet, count["Legendary"], self.legendary_mult, "legendary")
            final_mult *= self.apply_multiplier(epic_bet, count["Epic"], self.epic_mult, "epic")
            final_mult *= self.apply_multiplier(rare_bet, count["Rare"], self.rare_mult, "rare")
            final_mult *= self.apply_multiplier(refined_bet, count["Refined"], self.refined_mult, "refined")

            user_bablo *= final_mult

            embed = self.embed_pull_message(500, drops)
            print(count)
            print(final_mult)

        
        except Exception as e:
            print("Error in RarityGame: " + str(e))

    def apply_multiplier(self, bet, count, mult_factor, label):
        if bet > 0:
            if count == 0:
                return 0.75
            mult_val = abs(bet - count)
            print(f"mult val {label}: {mult_val}")
            return mult_factor * (1 / 2**mult_val)
        return 1
    

    def embed_pull_message(self, bablo, drops):
        _, itemName, mvp_rarity, mvp_url = drops[0]
        description = ""
        for drop in drops:
            itemID, itemName, rarity, url = drop

            current_emote = GConstants.RARITY_MAPPING[rarity][0]
            description += f"{current_emote} {itemName}\n"
        
        embed: discord.Embed = discord.Embed(description=description, url=mvp_url)
        embed.title = "The result of the pulls are..." 
        embed.colour = discord.Colour.from_str(GConstants.RARITY_MAPPING[mvp_rarity][0]) # TODO: make this cleaner later
        embed.set_footer(text=f"You still have {bablo} bablo left!")

        return embed


import asyncio, os
from dotenv import load_dotenv
from strinovabot import *
from discord.ext import commands
from components.games.gambling.gacha import Gacha
from components.games.gambling.strinovabanner import Banner
from components.games.gambling import mecha_angel
from components.games.gambling.banners import mecha_angel_drops
from db.GachaDb import GachaDb

async def main():

    load_dotenv()
    token = os.getenv('TOKEN')

    bot = Bot(token)
    
    gacha_db = GachaDb(r"src/components/games/Gambling/db/gacha.db")
    await gacha_db.clear()
    await gacha_db.create_default_tables()
    await gacha_db.create_banner_table("Mecha_Angel", mecha_angel_drops.drops)
    
    gacha = Gacha(bot, gacha_db)
    gacha.load_banner(Banner("Mecha Angel", mecha_angel.Drops, Gacha.DEFAULT_PROBABILITY))
    
    components = [gacha]
    
    await bot.load_cogs(components)
    await bot.init()

if __name__ == "__main__":
    asyncio.run(main())
   
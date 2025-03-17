import asyncio, os
from dotenv import load_dotenv
from strinovabot import *
from discord.ext import commands
from components.games.gambling.gacha import Gacha
from components.games.gambling.strinovabanner import Banner
from components.games.gambling import mecha_angel
from db.GachaDb import GachaDb


async def main():

    load_dotenv()
    token = os.getenv('TOKEN')

    bot = Bot(token)
    
    gacha_db = GachaDb(r"src/components/games/Gambling/db/gacha.db")
    await gacha_db.clear()
    await gacha_db.load_banners_from_csv(r"src/components/games/gambling/banners") 
    await gacha_db.create_default_tables()

    gacha = Gacha(bot, gacha_db)
    
    for banner in gacha_db.tables:
        gacha.load_banner(banner)

    components = [gacha]
    
    await bot.load_cogs(components)
    await bot.init()

if __name__ == "__main__":
    asyncio.run(main())
   
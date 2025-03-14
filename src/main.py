import asyncio, os
from dotenv import load_dotenv
from strinovabot import *
from discord.ext import commands
from components.games.Gambling.gacha import Gacha
from components.games.Gambling.strinovabanner import Banner
from components.games.Gambling import mecha_angel
from async_db import GachaDb 

async def main():
    load_dotenv()
    token = os.getenv('TOKEN')

    bot = Bot(token)
    
    gacha_db = GachaDb(r"src/components/games/Gambling/db/gacha.db")
    gacha = Gacha(bot, gacha_db)
    gacha.load_banner(Banner("Mecha Angel", mecha_angel.Drops, Gacha.DEFAULT_PROBABILITY))
    
    components = [gacha]
    await bot.load_cogs(components)
    await bot.init()
    

if __name__ == "__main__":
    asyncio.run(main())
   
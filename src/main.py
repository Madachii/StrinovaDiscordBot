import asyncio, os
from dotenv import load_dotenv
from strinovabot import *
from discord.ext import commands
from components.games.Gambling.gacha import Gacha
from components.games.Gambling.strinovabanner import Banner
from components.games.Gambling import mecha_angel

# --- Plans ---
# 1. The bot should run on components, gacha and all related should be added component, that inherits from some abstract class
#    and also make it so it's possible to have multiple of the same components, hence if you want double gacha
#    the gacha itself should require a database where to store stuff, so that multiple could run at same time
#    i'm not sure if multiple connections can be made to the same database? but that's for me to figuire out later
#    but ideally, only one component has access to a database

async def main():
    load_dotenv()
    token = os.getenv('TOKEN')

    bot = Bot(token)
    
    gacha = Gacha(Bot, None)
    gacha.load_banner(Banner("Mecha Angel", mecha_angel.Drops))
    
    components = [gacha]
    await bot.load_cogs(components)
    await bot.init()
    

if __name__ == "__main__":
    asyncio.run(main())
   
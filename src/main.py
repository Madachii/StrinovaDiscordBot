import asyncio, os
from dotenv import load_dotenv
from strinovabot import *
from components.games.gambling import Gacha, RarityGame, BannerManager
from db.GachaDb import GachaDb
import logging

logger = logging.getLogger(__name__)

async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    token = os.getenv('TOKEN')

    bot = Bot(token)
    
    gacha_db = GachaDb(r"src/components/games/Gambling/db/gacha.db")
    await gacha_db.clear()
    await gacha_db.create_default_tables()
    await gacha_db.load_banners_from_csv(r"src/components/games/gambling/banners") 
    logger.info("Recreated the database")

    gacha = Gacha(bot, gacha_db, logger)
    rarity_game = RarityGame(bot, gacha_db, logger)

    for banner in gacha_db.tables:
        uuid, name = banner
        BannerManager.load_banner(db=gacha_db, logger=logger, uuid=uuid, banner_name=name)
    
    components = [gacha, rarity_game]
    
    await bot.load_cogs(components)
    await bot.init()

if __name__ == "__main__":
    asyncio.run(main())
   
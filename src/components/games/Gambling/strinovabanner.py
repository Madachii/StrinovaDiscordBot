from components.games.gambling.items import Item, Rarity
from db import GachaDb
import secrets, bisect

class Banner:
    
    GUARANTEE_PROBABILITY = (0.017, 0.058, 0.243, 0.682) # TEMP
    RARITY_MAPPING = {0: "Legendary", 1: "Epic", 2: "Rare", 3: "Refined"}
    """Represents a Strinova Banner""" 

    def __init__(self, uuid, db: GachaDb, title: str, probabilities):

        self.uuid = uuid
        self.db = db
        self.title = title
        self.pool = {item.value: [] for item in Rarity}
         
   
    async def pull(self, weights):
        try:
            probability = {"0" : 0, "1" : 1, "2" : 2, "3" : 3}
            for x in range(10000):
                rng = secrets.SystemRandom().randrange(0, weights[-1])
                idx = bisect.bisect_right(weights, rng)
                probability[str(idx)] += 1
            
        except Exception as e:
            print(e) 
        banner_drops = await self.db.get_banner_drops(self.uuid, self.RARITY_MAPPING[idx])
        user_drop = banner_drops[rng % len(banner_drops)] 

        return user_drop
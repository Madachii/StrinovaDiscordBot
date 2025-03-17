from components.games.gambling.items import Item, Rarity
from db import GachaDb
import secrets, bisect
class Banner:
    RARITY_MAPPING = {0: "Legendary", 1: "Epic", 2: "Rare", 3: "Refined"}
    """Represents a Strinova Banner""" 

    def __init__(self, db: GachaDb, title: str, probabilities):

        self.db = db
        self.title = title
        self.pool = {item.value: [] for item in Rarity}
        self.weights = self.make_weights(probabilities)
         
    def make_weights(self, probabilities):
        if (sum(probabilities) != 1):
            raise ValueError(f"Failed to create the {self.title} banner, probabilities must add up to 1")
        
        weights = [round(prob * 10000) for prob in probabilities]
        
        cumulative_weights = []
        add = 0
        for w in weights:
            add += w
            cumulative_weights.append(add)
            
        return cumulative_weights
    
    async def pull(self):
        rng = secrets.SystemRandom().randrange(0, self.weights[-1])
        idx = bisect.bisect_right(self.weights, rng)

        banner_drops = await self.db.get_banner_drops(self.title, self.RARITY_MAPPING[idx])
        user_drop = banner_drops[rng % len(banner_drops)] 

        print(user_drop)
        return user_drop
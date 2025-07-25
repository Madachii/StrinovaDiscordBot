from components.games.gambling.items import Item, Rarity
from components.games.gambling.user import User 
from db import GachaDb
import secrets, bisect
import discord.ext

class Banner:
    
    RARITY_MAPPING = {0: "Legendary", 1: "Epic", 2: "Rare", 3: "Refined"} 

    def __init__(self, uuid, db: GachaDb, title: str, logger):
        self.uuid = uuid
        self.db = db
        self.title = title
        self.logger = logger
        self.pool = {item.value: [] for item in Rarity}
         
   
    async def get_drop(self, weights):
        rng = secrets.SystemRandom().randrange(0, weights[-1])
        idx = bisect.bisect_right(weights, rng)
            
        banner_drops = await self.db.get_banner_drops(self.uuid, self.RARITY_MAPPING[idx]) # TODO: hold them in memory instead of doing a query pull everytime
        user_drop = banner_drops[rng % len(banner_drops)] 

        return user_drop

    async def pull(self, ctx: discord.ext.commands.context.Context, user: User, banner, drops):
        print(user)
        try:
            user_drop = None
            difference = 0
            args = []

            if sum((user.weight_legendary, user.weight_epic, user.weight_rare, user.weight_refined)) != 100000:
                self.logger.warning(f"The weights got messed up for {ctx.author.name}")
                return

            if (user.legendary_pulls >= 80):
                user_drop = await self.get_drop(self.cumulative_weights((100000, 0, 0, 0)))
                user.weight_legendary, user.legendary_pulls, difference = await self.legendary_pull(user.weight_legendary, legendary_pulls=0, pity=True)
                    
            elif (user.epic_pulls >= 30):
                user_drop = await self.get_drop(self.cumulative_weights((0,100000, 0, 0)))
                user.weight_epic, user.epic_pulls, difference = await self.epic_pull(user.weight_epic, epic_pulls = 0, pity=True)

            elif (user.rare_pulls >= 10):
                user_drop = await self.get_drop(self.cumulative_weights((0,0,100000, 0)))
                user.weight_rare, user.rare_pulls, difference = await self.rare_pull(user.weight_rare, rare_pulls=0, pity=True)
                
            else:
                cumulative_weights = self.cumulative_weights((user.weight_legendary, user.weight_epic, user.weight_rare, user.weight_refined)) 
                user_drop = await self.get_drop(cumulative_weights)
                
                _, _, rarity, _ = user_drop
                extra_weight = extra_pulls = extra_difference = 0
                if rarity == "Legendary":
                    extra_weight, extra_pulls, extra_difference = await self.legendary_pull(user.weight_legendary, legendary_pulls=0, pity=True)
                else:
                    extra_weight, extra_pulls, extra_difference = await self.legendary_pull(user.weight_legendary, user.legendary_pulls + 1, self.db.pity_bonus_legendary, pity=False)

                user.weight_legendary = extra_weight
                user.legendary_pulls = extra_pulls
                difference += extra_difference
                
                if rarity == "Epic":
                    extra_weight, extra_pulls, extra_difference = await self.epic_pull(user.weight_epic, epic_pulls = 0, pity=True)
                else:
                    extra_weight, extra_pulls, extra_difference = await self.epic_pull(user.weight_epic, user.epic_pulls + 1, self.db.pity_bonus_epic, pity=False)

                user.weight_epic = extra_weight
                epic_pulls = extra_pulls
                difference += extra_difference

                if rarity == "Rare":
                    extra_weight, extra_pulls, extra_difference = await self.rare_pull(user.weight_rare, rare_pulls=0, pity=True)
                else:
                    extra_weight, extra_pulls, extra_difference = await self.rare_pull(user.weight_rare, user.rare_pulls + 1, self.db.pity_bonus_rare, pity=False)
                
                user.weight_rare = extra_weight
                user.rare_pulls = extra_pulls
                difference += extra_difference

            user.weight_refined -= difference

            drops.append(user_drop)
            return user 

        except Exception as e:
            print(e)

    # TODO: clean this code... alot.
    async def legendary_pull(self, weight_legendary = 0, legendary_pulls = 0, weight_pity = 0, pity = False):
        post_weight = post_pulls = difference = 0
        if pity:
            post_weight = self.db.weight_legendary
            difference += self.db.weight_legendary - weight_legendary
        else:
            post_weight = weight_legendary + weight_pity
            post_pulls = legendary_pulls
            difference += self.db.pity_bonus_legendary
        
        return (post_weight, post_pulls, difference)
    
    
    async def epic_pull(self, weight_epic = 0, epic_pulls = 0, weight_pity = 0, pity = False):
        post_weight = post_pulls = difference = 0
        if pity:
            post_weight = self.db.weight_epic
            difference += self.db.weight_epic - weight_epic 
        else:
            post_weight = weight_epic + weight_pity
            post_pulls = epic_pulls
            difference += self.db.pity_bonus_epic

        return (post_weight, post_pulls, difference)
        
    async def rare_pull(self, weight_rare = 0, rare_pulls = 0, weight_pity = 0, pity = False):
        post_weight = post_pulls = difference = 0
        if pity:
            post_weight = self.db.weight_rare
            difference += self.db.weight_rare - weight_rare 
        else:
            post_weight = weight_rare + weight_pity
            post_pulls = rare_pulls
            difference += self.db.pity_bonus_rare

        return (post_weight, post_pulls, difference)

    def cumulative_weights(self, weights):
        cumulative_weights = []
        add = 0
        for w in weights:
            add += w
            cumulative_weights.append(add)
        
        return cumulative_weights
    
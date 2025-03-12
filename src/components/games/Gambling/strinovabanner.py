from components.games.Gambling.items import Item, Rarity

DEFAULT_PROBABILITY = (0.0065, 0.05, 0.24, 0.7035)

class Banner:
    """Represents a Strinova Banner""" 
    def __init__(self, title, drop):
        self.title = title
        self.pool = {item.value: [] for item in Rarity}

        for item in drop:
            if not isinstance(item, Item):
                print(f"{item} is not an valid item")
                continue

            self.pool[f"{item.rarity.value}"].append(item)
        
        print(f"The avaliable legendary's in this banner are: {[x.name for x in self.pool['Legendary']]}") 
        
        
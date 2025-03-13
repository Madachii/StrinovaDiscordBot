from components.games.Gambling.items import Item, Rarity


class Banner:
    """Represents a Strinova Banner""" 

    def __init__(self, title, drop, probabilities):

        self.title = title
        self.pool = {item.value: [] for item in Rarity}
        self.weights = self.make_weights(probabilities)

        for item in drop:
            if not isinstance(item, Item):
                raise ValueError(f"{item} is not a  valid item")

            self.pool[f"{item.rarity.value}"].append(item)
        
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
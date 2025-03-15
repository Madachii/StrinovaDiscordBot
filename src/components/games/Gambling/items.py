from enum import Enum

class Rarity(Enum):
    LEGENDARY = "Legendary"
    EPIC = "Epic"
    RARE = "Rare"
    REFINED = "Refined"

class Item_Type(Enum):
    OUTFIT = "Outfit"
    WEAPON_SKIN = "Weapon_Skin"
    CHIP_SKIN = "Chip_Skin"
    SPRAY = "Spray"
    EMOTE = "Emote"
    VOICE = "Voice"
    
class Agent(Enum):
    KOKONA = "Kokona"
    YVETTE = "Yvette"
    FUSCHIA = "Fuschia"
    REIICHI = "Reiichi"
    MADDELENA = "Maddelena"
    KANAMI = "Kanami"
    BAIMO = "Bai Mo"
    NOBUNAGA = "Nobunaga"
    MEREDITH = "Meredith"
    LAWINE = "Lawine"
    AUDREY = "Audrey"
    MICHELE = "Michele"
    CELESTIA = "Celestia"
    MING = "Ming"
    EIKA = "Eika"

class Item:
    def __init__(self, name: str, rarity: Rarity, img_url: str = None, item_type: Item_Type = None, agent: Agent = None): # Make None be a "for all" value later
        self.name = name
        self.agent = agent
        self.rarity = rarity
        self.item_type = item_type
        self.img_url = img_url 
        
# class Outfit(Item):
#     def __init__(self, name, rarity):
#         super().__init__(name, rarity, "Outfit")
         
# class Weapon_Skin(Item):
#     def __init__(self, name, rarity):
#         super().__init__(name, rarity, "Weapon_Skin")
          
# class Chip_Skin(Item):
#     def __init__(self, name, rarity):
#         super().__init__(name, rarity, "Chip_Skin")
        
# class Spray(Item):
#     def __init__(self, name, rarity):
#         super().__init__(name, rarity, "Spray")
        
# class Emote(Item):
#     def __init__(self, name, rarity):
#         super().__init__(name, rarity, "Emote")

# class Voices(Item):
#     def __init__(self, name, rarity):
#         super().__init__(name, rarity, "Voices")

# ITEM_TYPES = (Outfit, Weapon_Skin, Chip_Skin, Spray, Emote, Voices)
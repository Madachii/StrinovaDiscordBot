from components.games.gambling.items import *

Drops = {
    Item("Mecha Angel", Rarity.LEGENDARY, Item_Type.OUTFIT, Agent.KOKONA),
    Item("Heavenly Nexus", Rarity.LEGENDARY, Item_Type.WEAPON_SKIN, Agent.KOKONA),
    Item("Tactical Training", Rarity.EPIC, Item_Type.OUTFIT, Agent.YVETTE),
    Item("Shadow Strike", Rarity.EPIC, Item_Type.OUTFIT, Agent.FUSCHIA),
    Item("Handyman", Rarity.EPIC, Item_Type.OUTFIT, Agent.REIICHI),
    Item("Grizzly Camo", Rarity.EPIC, Item_Type.WEAPON_SKIN, Agent.YVETTE),
    Item("Forest Kit", Rarity.EPIC, Item_Type.WEAPON_SKIN, Agent.REIICHI),
    Item("Ocean Hunter", Rarity.EPIC, Item_Type.WEAPON_SKIN, Agent.FUSCHIA),
    Item("Drink Collector", Rarity.RARE, Item_Type.CHIP_SKIN),
    Item("Solitude", Rarity.RARE, Item_Type.CHIP_SKIN),
    Item("Joyful Free Diving", Rarity.RARE, Item_Type.CHIP_SKIN),
    Item("Boxer", Rarity.RARE, Item_Type.SPRAY),
    Item("The Bait", Rarity.RARE, Item_Type.SPRAY),
    Item("Fall Back", Rarity.RARE, Item_Type.SPRAY),
    Item("Mint Summer", Rarity.RARE, Item_Type.OUTFIT, Agent.KANAMI),
    Item("Core Conflict", Rarity.RARE, Item_Type.OUTFIT, Agent.MEREDITH),
    Item("Sakura Blizzard", Rarity.RARE, Item_Type.OUTFIT, Agent.YVETTE), # I need to remember to add a check, outfit needs a agent, same with weapon 
    Item("Echo of Doom", Rarity.RARE, Item_Type.OUTFIT, Agent.LAWINE),
    Item("Taxi Hustle", Rarity.RARE, Item_Type.OUTFIT, Agent.KOKONA),
    Item("Speed Racer", Rarity.RARE, Item_Type.OUTFIT, Agent.BAIMO),
    Item("Thorns of Glory", Rarity.RARE, Item_Type.OUTFIT, Agent.NOBUNAGA),
    Item("Blueberry Milk", Rarity.RARE, Item_Type.OUTFIT, Agent.MADDELENA),
    Item("Spring Special", Rarity.RARE, Item_Type.OUTFIT, Agent.AUDREY),
    Item("Storm Warning", Rarity.RARE, Item_Type.OUTFIT, Agent.MICHELE),
    Item("Manga Star", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.BAIMO),
    Item("Golden Surge", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.YVETTE),
    Item("House of Cards", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.AUDREY),
    Item("Aviary", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.NOBUNAGA),
    Item("Astrologist", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.MADDELENA),
    Item("House of Cards", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.KOKONA),
    Item("House of Cards", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.KANAMI),
    Item("House of Cards", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.MEREDITH),
    Item("Chibi World", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.LAWINE),
    Item("Maneki-Neko", Rarity.RARE, Item_Type.WEAPON_SKIN, Agent.MICHELE),
    Item("Kokona - Here Comes the Veteran", Rarity.REFINED, Item_Type.EMOTE),
    Item("Meredith - Just Right", Rarity.REFINED, Item_Type.EMOTE),
    Item("Meredith - Almost There", Rarity.REFINED, Item_Type.EMOTE),
    Item("Kokona - Troubled", Rarity.REFINED, Item_Type.EMOTE),
    Item("Celestia - Exhausted", Rarity.REFINED, Item_Type.EMOTE),
    Item("Strinova Blue", Rarity.REFINED, Item_Type.CHIP_SKIN),
    Item("Restoration", Rarity.REFINED, Item_Type.CHIP_SKIN),
    Item("Tactical - Town", Rarity.REFINED, Item_Type.CHIP_SKIN),
    Item("Stairs of Evolution", Rarity.REFINED, Item_Type.CHIP_SKIN),
    Item("Cutting-Edge Weapon", Rarity.REFINED, Item_Type.CHIP_SKIN),
    Item("Doggy", Rarity.REFINED, Item_Type.SPRAY),
    Item("No Skipping", Rarity.REFINED, Item_Type.SPRAY),
    Item("Mass-Energy Equivale", Rarity.REFINED, Item_Type.SPRAY),
    Item("Inverted Fragment", Rarity.REFINED, Item_Type.SPRAY),
    Item("Target Locked", Rarity.REFINED, Item_Type.SPRAY),
    Item("Take a Bath", Rarity.REFINED, Item_Type.SPRAY),
    Item("Ultimate: My Gift", Rarity.REFINED, Item_Type.VOICE, Agent.CELESTIA),
    Item("Elimination: All the Same", Rarity.REFINED, Item_Type.VOICE, Agent.YVETTE),
    Item("Elimination: You are All Pray", Rarity.REFINED, Item_Type.VOICE, Agent.FUSCHIA),
    Item("Ultimate: Lock & Loaded", Rarity.REFINED, Item_Type.VOICE, Agent.BAIMO),
    Item("Astral Blessing - Cloud", Rarity.REFINED, Item_Type.OUTFIT, Agent.CELESTIA),
    Item("Nightingale - Sprout", Rarity.REFINED, Item_Type.OUTFIT, Agent.KANAMI),
    Item("Wisdom - Litmus", Rarity.REFINED, Item_Type.OUTFIT, Agent.MEREDITH),
    Item("Rebel - Dusk", Rarity.REFINED, Item_Type.OUTFIT, Agent.MING),
    Item("Ruined Blade - Sand", Rarity.REFINED, Item_Type.OUTFIT, Agent.LAWINE),
    Item("Trace - Mountain", Rarity.REFINED, Item_Type.OUTFIT, Agent.KOKONA),
    Item("School Uniform - Taro", Rarity.REFINED, Item_Type.OUTFIT, Agent.EIKA),
    Item("Infiltrator - Seabed", Rarity.REFINED, Item_Type.OUTFIT, Agent.FUSCHIA),
    Item("Unfettered - Picnic", Rarity.REFINED, Item_Type.OUTFIT, Agent.BAIMO),
    Item("Guardian - Ash", Rarity.REFINED, Item_Type.OUTFIT, Agent.NOBUNAGA),
    Item("Violet Gold", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.EIKA),
    Item("Prisma", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.BAIMO),
    Item("Vigilance", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.NOBUNAGA),
    Item("Wave Surfer", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.KOKONA),
    Item("Faith", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.KANAMI),
    Item("Chimera", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.FUSCHIA),
    Item("Illusion", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.CELESTIA),
    Item("Tidal Wave", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.MEREDITH),
    Item("Neon", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.LAWINE),
    Item("Camo", Rarity.REFINED, Item_Type.WEAPON_SKIN, Agent.MING)
}

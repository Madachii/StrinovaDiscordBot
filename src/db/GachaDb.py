from typing import List, Tuple
from db.DbManager import DbManager
from components.games.gambling.items import Item
import os, csv
        
# TODO: Make a single query with transcation
class GachaDb(DbManager):
    default_bablo = 1200
    weight_legendary, weight_epic, weight_rare, weight_refined = (650, 5000, 24000, 70350)
    pity_bonus_legendary, pity_bonus_epic, pity_bonus_rare = (13, 37, 30)
    
    def __init__(self, path: str):
        super().__init__(path)
        self.tables = [] 
        # TODO: replace all the static names with variables
        
        
    # TODO: replace all the f strings with proper sql ? tokens
    async def add_drops_to_banners(self, uuid,  name, drops: List[Tuple]): 
        cmd = f"""
            CREATE TABLE IF NOT EXISTS banner_drops
            (
                itemID INTEGER PRIMARY KEY AUTOINCREMENT,
                bannerID BLOB NOT NULL,
                itemName TEXT NOT NULL,
                rarity TEXT NOT NULL,
                url TEXT UNIQUE,
                UNIQUE(bannerID, itemName, rarity, url)
            );
            """
        await super().commit_execute(cmd)
        
        cmd = f""" INSERT OR IGNORE INTO active_banners (bannerID, bannerName) VALUES (?, ?)"""
        await super().commit_execute(cmd, (uuid, name))
        
        uuid_and_drops = [(uuid, ) + tuple(drop) for drop in drops]
        # TODO: make sure the items we add into the database are correct, aka check each item for specific specifiers 
        cmd = f"""INSERT OR IGNORE INTO banner_drops (bannerID, itemName, rarity, url) VALUES (?, ?, ?, ?)"""
        await super().executemany(cmd, uuid_and_drops)

        self.tables.append((uuid,name))

    async def create_default_tables(self):
        cmd = ""
        
        # the weights are cumulative, generated from the default probability of
        # DEFAULT_PROBABILITY = (0.0065, 0.05, 0.24, 0.7035)
        cmd += f""" 
            CREATE TABLE IF NOT EXISTS USERS
            (
                userID BIGINT PRIMARY KEY NOT NULL,
                bablo INTEGER DEFAULT {GachaDb.default_bablo},
                basestring INTEGER DEFAULT 0,
                active_banner BLOB NOT NULL,
                legendary_pulls INTEGER DEFAULT 0,
                epic_pulls INTEGER DEFAULT 0,
                rare_pulls INTEGER DEFAULT 0,
                weight_legendary INTEGER DEFAULT {self.weight_legendary},
                weight_epic INTEGER DEFAULT {self.weight_epic},
                weight_rare INTEGER DEFAULT {self.weight_rare},
                weight_refined INTEGER DEFAULT {self.weight_refined}
            );
            """
        cmd +=  """
            CREATE TABLE IF NOT EXISTS ITEMS
            (
                itemID INTEGER PRIMARY KEY,
                itemName TEXT NOT NULL,
                rarity TEXT NOT NULL,
                agent TEXT,
                urlLink TEXT UNIQUE
            ); 
            """           
        # TODO: create index for userID, hence we'll often get all of the items for a specific user id
        cmd += """
            CREATE TABLE IF NOT EXISTS INVENTORY
            (
                inventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                userID BIGINT NOT NULL,
                bannerID INTEGER NOT NULL,
                itemID INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY(userID) REFERENCES USERS(userID) ON DELETE CASCADE,
                FOREIGN KEY(itemID) REFERENCES ITEMS(itemID),
                UNIQUE(bannerID, itemID)
            );  
        """

        cmd += """
            CREATE TABLE IF NOT EXISTS ACTIVE_BANNERS
            (
                bannerID BLOB PRIMARY KEY NOT NULL,
                bannerName TEXT NOT NULL,
                UNIQUE(bannerID, bannerName) 
            );
        """

        await super().commit_executescript(cmd)

    async def load_banners_from_csv(self, path: str):
        files = os.listdir(path)
        
        for file in files:
            name, extension = os.path.splitext(file)
            
            if (extension != ".csv"):
                continue
            
            with open(f"{path}/{name + extension}", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                uuid = await super().generate_uuid(name)
                await self.add_drops_to_banners(uuid, name, reader) 
            
            
    async def get_banner_drops(self, uuid, rarity: str = "ALL"):
        cmd = ""
        cmd += f"""
            SELECT itemID, itemName, rarity, url FROM banner_drops
        """
        if (rarity != "ALL"):
            cmd += f"WHERE rarity = '{rarity}' AND bannerID = '{uuid}'" 
        
        result = await super().execute(cmd) 
        
        return result

    # I don't remember the basestring you get from getting the same skin ;-;
    async def add_drop(self, discord_id, banner_id, item_id, rarity):
        await self.add_user(discord_id)

        cmd = ""
        cmd += f""" 
            INSERT INTO INVENTORY(userID, bannerID, itemID, quantity) VALUES (?, ?, ?, 1)
            ON CONFLICT(bannerID, itemID) DO UPDATE SET quantity = quantity + excluded.quantity
        """
        
        return await super().commit_execute(cmd, (discord_id, banner_id, item_id))

    async def add_user(self, discord_id, active_banner = None, starting_bablo = default_bablo):
        cmd = ""

        if (active_banner is None):
            cmd = "SELECT bannerID FROM ACTIVE_BANNERS ORDER BY ROWID DESC LIMIT 1;"
            result = await super().execute(cmd)
            active_banner = result[0][0]

        cmd = """
        INSERT OR IGNORE INTO USERS (userID, bablo, active_banner) VALUES (?, ?, ?)
        """
        await super().commit_execute(cmd, (discord_id, starting_bablo, active_banner))
        
    async def update_user(self, discord_id, args: List[Tuple[str, int]]):
        cmd = ""
        
        for arg in args:
            var, val = arg
            cmd += f"UPDATE USERS SET {var} = {val} WHERE userID = {discord_id};"
        
        await self.commit_executescript(cmd)

    async def get_inv(self, discord_id):
        cmd = ""
        cmd += f"""
        SELECT banner_drops.itemName, banner_drops.rarity, USERS.bablo 
        FROM inventory 
        JOIN banner_drops ON inventory.itemID = banner_drops.itemID 
        JOIN USERS ON inventory.userID = USERS.userID
        WHERE INVENTORY.userID = ?
        """

        return await super().execute(cmd, (discord_id,))
        
    async def get_user_data(self, discord_id, *params):
        cmd = ""
        column = []
        if not params:
            column = ["*"]
        else:    
            column = [f"USERS.{param}" for param in params]

        cmd += f"""
        SELECT {', '.join(column)} FROM USERS WHERE userID = ?
         """

        return await super().execute(cmd, (discord_id,))
        
    async def clear(self):
        cmd = ""
        
        for table in self.tables:
            cmd += f"DROP TABLE IF EXISTS {table}"
        
        cmd +=  """
                DROP TABLE IF EXISTS active_banners;
                DROP TABLE IF EXISTS INVENTORY;
                DROP TABLE IF EXISTS USERS;
                DROP TABLE IF EXISTS ITEMS;
                """
        
        await super().commit_executescript(cmd)
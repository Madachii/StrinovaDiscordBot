from typing import List, Tuple
from db.DbManager import DbManager
from components.games.gambling.items import Item
import os, csv
        
class GachaDb(DbManager):
    default_bablo = 1200
    def __init__(self, path: str):
        super().__init__(path)
        self.tables = [] 
        
    # TODO: replace all the f strings with proper sql ? tokens
    async def create_banner_table(self, name, drops: List[Tuple]): 
        cmd = f"""
            CREATE TABLE IF NOT EXISTS {name}
            (
                itemID INTEGER PRIMARY KEY AUTOINCREMENT,
                itemName TEXT NOT NULL,
                rarity TEXT NOT NULL,
                url TEXT UNIQUE,
                UNIQUE(itemName, rarity, url)
            );
            """
        await super().commit_execute(cmd)
        # TODO: make sure the items we add into the database are correct, aka check each item for specific specifiers 
        cmd = f"""INSERT OR IGNORE INTO {name} (itemName, rarity, url) VALUES (?, ?, ?)"""
        await super().executemany(cmd, drops)

        self.tables.append(name)

    async def create_default_tables(self):
        cmd = ""
        cmd += f""" 
            CREATE TABLE IF NOT EXISTS USERS
            (
                userID BIGINT PRIMARY KEY NOT NULL,
                bablo INTEGER DEFAULT {GachaDb.default_bablo},
                active_banner INTEGER DEFAULT {len(self.tables) - 1},
                UNIQUE(userID)
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
        
        cmd += """
            CREATE TABLE IF NOT EXISTS INVENTORY
            (
                inventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                userID BIGINT NOT NULL,
                itemID INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY(userID) REFERENCES USERS(userID) ON DELETE CASCADE,
                FOREIGN KEY(itemID) REFERENCES ITEMS(itemID),
                UNIQUE(itemID)
            );  
        """

        cmd += """
            CREATE TABLE IF NOT EXISTS ACTIVE_TABLES
            (
                bannerID INTEGER PRIMARY KEY AUTOINCREMENT,
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
                await self.create_banner_table(name, reader) 
            
            
    async def get_banner_drops(self, table: str, rarity: str = "ALL"):
        cmd = ""
        cmd += f"""
            SELECT * FROM {table}
        """
        if (rarity != "ALL"):
            cmd += f"WHERE rarity = '{rarity}'" # TODO: need to make a system to limit these, just writing pure strings is bad
        
        result = await super().execute(cmd) 
        
        return result

    async def add_drop(self, discord_id, item_id):
        await self.add_user(discord_id)

        cmd = ""
        cmd += f"""
            INSERT INTO INVENTORY(userID, itemID, quantity) VALUES (?, ?, 1)
            ON CONFLICT(itemID) DO UPDATE SET quantity = quantity + excluded.quantity
        """
        
        return await super().commit_execute(cmd, (discord_id, item_id))
    async def add_user(self, discord_id, starting_bablo = default_bablo):
        # TODO: make sure discord_id is a valid one
        await super().commit_execute(
            f"""
            INSERT OR IGNORE INTO USERS (userID, bablo) VALUES ({discord_id}, {starting_bablo})
            """
        )
        
    async def get_user(self, discord_id):
        result = await super().execute(
            f"""
            SELECT * FROM USERS WHERE userID = {discord_id}
            """
        )
        
        return result

    async def get_inv(self, discord_id, banner):
        cmd = ""
        cmd += f"""
        SELECT {banner}.itemname FROM inventory JOIN {banner} ON INVENTORY.itemID = {banner}.itemID WHERE INVENTORY.userID = ?
        """
        
        return await super().execute(cmd, (discord_id,))
        
    async def add_bablo(self, discord_id, amount):
        cmd = ""
        cmd += """
        INSERT INTO USERS(userID, bablo) VALUES (?, ?)
        ON CONFLICT(userID) DO UPDATE SET bablo = bablo + excluded.bablo;
        """
        await super().commit_execute(cmd, (discord_id, amount))

    async def subtract_bablo(self, discord_id, amount):
        cmd = ""
        cmd += """
        UPDATE USERS SET bablo = bablo - ? WHERE userID = ?
        """
        
        await super().commit_execute(cmd, (amount, discord_id))
        
    async def get_user_data(self, discord_id, *params):
        column = [f"USERS.{param}" for param in params]

        cmd = ""
        cmd += f"""
        SELECT {', '.join(column)} FROM USERS WHERE userID = ?
        """

        return await super().execute(cmd, (discord_id,))
        
    async def clear(self):
        cmd = ""
        
        for table in self.tables:
            cmd += f"DROP TABLE IF EXISTS {table}"
        
        cmd +=  """
                DROP TABLE IF EXISTS INVENTORY;
                DROP TABLE IF EXISTS USERS;
                DROP TABLE IF EXISTS ITEMS;
                """
        
        await super().commit_executescript(cmd)
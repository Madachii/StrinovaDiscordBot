import aiosqlite
from typing import List, Tuple
from db.DbManager import DbManager
from components.games.gambling.items import Item
        
class GachaDb(DbManager):
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
        cmd += """ 
            CREATE TABLE IF NOT EXISTS USERS
            (
                userID BIGINT PRIMARY KEY NOT NULL,
                bablo INTEGER DEFAULT 0
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
                userID BIGINT,
                itemID INTEGER,
                FOREIGN KEY(userID) REFERENCES USERS(userID) ON DELETE CASCADE,
                FOREIGN KEY(itemID) REFERENCES ITEMS(itemID)
            );  
        """

        await super().commit_executescript(cmd)

    async def get_banner_drops(self, table: str, rarity: str = "ALL"):
        cmd = ""
        cmd += f"""
            SELECT * FROM {table}
        """
        if (rarity != "ALL"):
            cmd += f"WHERE rarity = '{rarity}'" # TODO: need to make a system to limit these, just writing pure strings is bad
        
        result = await super().execute(cmd) 
        
        return result

    async def add_user(self, discord_id, starting_bablo = 0):
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
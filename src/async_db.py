import aiosqlite

class DbManager:
    def __init__(self, path: str):
        self.path = path
        self.connection = None
        self.cursor = None
    
    async def create_db(self, args: str):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(args)
            await db.commit()
            

    async def close(self):
        if self.cursor:
            await self.cursor.close()
        if self.connection:
            await self.connection.close()
        
        
class GachaDb(DbManager):
    def __init__(self, path: str):
        self.tables = """CREATE TABLE IF NOT EXISTS inventory
                    (
	                    userID INTEGER PRIMARY KEY NOT NULL,
                        backpackID int UNIQUE,
	                    points INTEGER DEFAULT 0
                    );
                    """
    
    async def add_drop():
        pass
    
    async def get_stats(user):
        pass
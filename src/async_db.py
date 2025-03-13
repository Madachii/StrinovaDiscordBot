import aiosqlite

class DbManager:
    def __init__(self, path: str):
        self.path = path
        self.connection = None
        self.cursor = None
    
    async def init_db(self):
        self.connection = await aiosqlite.connect(self.path)
        self.cursor = await self.connection.cursor()
        
    async def create_db(self, args: str):
        await self.init_db()
        await self.cursor.execute(args)
        await self.connection.commit()
            
    async def execute(self, args: str):
        await self.cursor.execute(args)
        await self.connection.commit()
        
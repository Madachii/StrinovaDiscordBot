import aiosqlite
from typing import List, Tuple

class DbManager:
    def __init__(self, path: str):
        self.path = path
        self.connection = None
        self.cursor = None
    
    async def commit_execute(self, args: str, params: Tuple = ()):
        async with aiosqlite.connect(self.path) as db:
            async with await db.execute(args, params) as cursor:
                result = await cursor.fetchall()   
            await db.commit()
        
        return result
    
    async def commit_executescript(self, args: str, params: Tuple = ()):
        async with aiosqlite.connect(self.path) as db:
            async with await db.executescript(args) as cursor:
                result = await cursor.fetchall()    
            await db.commit()
        
        return result
            
    async def execute(self, args: str, params: Tuple = ()):
        async with aiosqlite.connect(self.path) as db:
            async with await db.execute(args, params) as cursor:
                result = await cursor.fetchall()

        return result

    async def executemany(self, args: str, items: List[tuple]):
        async with aiosqlite.connect(self.path) as db:
            async with await db.executemany(args, items) as cursor:
                result = await cursor.fetchall()
            await db.commit()

        return result
    
    async def close(self):
        if self.cursor:
            await self.cursor.close()
        if self.connection:
            await self.connection.close()
        
        
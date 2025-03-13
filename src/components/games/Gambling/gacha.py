import discord
import aiosqlite
import discord.ext.commands
from components.component import Component
from components.games.Gambling.strinovabanner import Banner
from discord.ext import commands
from async_db import DbManager
import discord.ext

class Gacha(commands.Cog, Component):
    DEFAULT_PROBABILITY = (0.0065, 0.05, 0.24, 0.7035)

    def __init__(self, bot, db: DbManager):
        self.bot = bot
        self.banners = []
        self.db = db

    def load_banner(self, banner: Banner):
        self.banners.append(banner)
        
    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f'Hello {member.name}~')
        
    @commands.command()
    async def pull(self, ctx, *, member: discord.Member = None):
        await ctx.send("Pulled")
        pass
        
    @commands.command()
    async def addp(self, ctx: discord.ext.commands.context.Context):
        try:
            await self.db.cursor.execute(
                """
                INSERT INTO money (userID, points) VALUES(?, ?) 
                ON CONFLICT(userID) DO UPDATE SET points = points + ?;
                """, (ctx.author.id, 10, 10)
            )
            await self.db.connection.commit()
            
            
            # Execute the SELECT query to get the points of the user
            await self.db.cursor.execute(
                """
                SELECT points FROM money WHERE userID = ?;
                """, (ctx.author.id,)
            )
            
            result = await self.db.cursor.fetchone()
            
            print(result)
            
            if result:
                print(result[0])
        except Exception as e:
            # Catch any exception and print it to the console
            print(f"An error occurred: {e}")


    def help(self):
        # Implement the help method here, as Component's help is abstract
        return "This is the help for the Gacha class"
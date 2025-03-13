import discord
from discord.ext import commands
from components.component import Component 

class Bot:
    def __init__(self, token: str):
        self.running = False 
        self.token = token
        
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        @self.bot.event
        async def on_ready():
            print("worked yey")


        @self.bot.command()
        async def test(ctx):
            print("asd")
            pass
    

    async def init(self):
        await self.bot.start(self.token) # TODO: make the main loop myself, instead of just using theirs
    
    async def load_cog(self, component):
        await self.bot.add_cog(component)
    
    async def load_cogs(self, components):
        for comp in components:
            try:
                await self.load_cog(comp)
            except Exception as e:
                print(f"{comp} failed to load: {e}")
    
    async def load_cog_db(self, component, db):
        await self.bot.add_cog(component(self.bot, db))
        
    async def remove_cog(self, component):
        await self.bot.remove_cog(component.__cog_name__)


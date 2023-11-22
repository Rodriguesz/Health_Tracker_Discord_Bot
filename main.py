from modules.client import MyClient
from decouple import config
import discord


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
client = MyClient(intents=intents)

TOKEN = config("TOKEN")
client.run(TOKEN)
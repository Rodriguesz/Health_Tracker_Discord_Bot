from discord.ext import commands
import os

class MyClient(commands.Bot):
    def __init__(self, intents) -> None:
        super().__init__(intents=intents, command_prefix='$', help_command=None)
        
    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        # Carrega todas as extensões na pasta 'commands'
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                cog = f'commands.{filename[:-3]}'  # Remove a extensão '.py'
                await self.load_extension(cog)
                
        
        for guild in self.guilds:
            print(guild)
            # Encontrar o primeiro canal de texto com permissão de enviar mensagens
            text_channel = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages), None)

            if text_channel:
                await text_channel.send("O pai ta na área")
        
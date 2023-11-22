from discord.ext import commands
from data.database import DatabaseManager
import discord
from modules.embeds import EmbedCreation

class UserCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db_manager = DatabaseManager()
        self.user_infos = {
            '📏': 'Altura',
            '⚖️': 'Peso',
            '🧓': 'idade',
            '🏳️‍⚧️': 'Gênero',
            '💪': 'Nível de atividade'
        }
        self.activity_levels = {
            '💤': 'Sedentário',
            '😊': 'Leve',
            '😁': 'Moderado',
            '🔥': 'Ativo',
            '🐀': 'Muito Ativo'
        }
        
        self.gender_emoji = {
            '♂': 'Masculino',
            '♀': 'Feminino'
        }

        
    @commands.command(name='atualizar', help='Atualiza um dos valores do perfil do usuário.')
    async def atualizar(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        discord_id = ctx.author.id
        existing_user = self.db_manager.get_user(guild_id, discord_id)
        
        if existing_user:
            await ctx.send('Qual campo vc deseja alterar?')
            message = await ctx.send(embed= await EmbedCreation.user_embed(self.user_infos))
            for emoji in self.user_infos:
                await message.add_reaction(emoji)
            
            #o user é fornecido automaticamente pelo discord.py quando o evento é acionado  
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in self.user_infos)
            att_field = self.user_infos[str(reaction.emoji)]

            succes = True
            match att_field:
                case 'Altura':
                    succes = await self.change_height(ctx, guild_id, discord_id)
                case 'Peso':
                    succes = await self.change_weight(ctx, guild_id, discord_id)
                case 'idade':
                    succes = await self.change_age(ctx, guild_id, discord_id)
                case 'Gênero':
                    await self.change_gender(ctx, guild_id, discord_id)
                case 'Nível de atividade':
                    await self.change_activity_level(ctx, guild_id, discord_id)
            if succes:
                await ctx.send('Valores alterados com sucesso :white_check_mark:')
            else:
                await ctx.send('Nenhum valor foi alterado :x:')
            
            
        else:
            await ctx.send('Você ainda não está registrardo. Digite $registrar e informe seus dados!')
            
    @commands.command(name='perfil', help='Retorna as informações do usuário')
    async def perfil(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        discord_id = ctx.author.id
        existing_user = self.db_manager.get_user(guild_id, discord_id)
        if existing_user:
            await ctx.send(embed=EmbedCreation.create_user_embed(ctx, existing_user))
        else:
            await ctx.send('Você ainda não está registrado. Digite $registrar e informe seus dados!')
            
    @commands.command(name='comandos', help='Lista os comandos disponíveis.')
    async def comandos(self, ctx: commands.Context) -> None:
        help_message = "**Lista de Comandos:**\n"

        for command in self.bot.commands:
            if not command.hidden:
                help_message += f"${command.name}: {command.help}\n"

        try:
            await ctx.author.send(help_message)
            await ctx.send("A mensagem de ajuda foi enviada para a sua DM.")
        except discord.Forbidden:
            await ctx.send("Não consegui te enviar a mensagem Zé. Verifique se suas mensagens diretas estão ativadas.")
        
        
    
    async def change_height(self, ctx, guild_id, discord_id):
        try:
            await ctx.send('Informe o novo valor de altura:')
            height_content = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            height = height_content.content.strip()
            if ',' in height:
                height = height.replace(',', '')
            height = int(height)
            
            await self.db_manager.update_column(guild_id, discord_id, 'height', height)
            return True
        except ValueError:
            await ctx.send('Os valores inseridos são inválidos')
            return False
            
    async def change_weight(self, ctx, guild_id, discord_id):
        try:
            await ctx.send('Informe o novo valor de peso:')
            weight_content = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            weight = weight_content.content.strip()
            if ',' in weight:
                weight = weight.replace(',', '.')
            weight = float(weight)
            
            await self.db_manager.update_column(guild_id, discord_id, 'weight', weight)
            return True
        except ValueError:
            await ctx.send('Os valores inseridos são inválidos')
            return False
        
    async def change_age(self, ctx, guild_id, discord_id):
        try:
            await ctx.send('Por favor, digite sua idade:')
            age = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
            age = int(age.content.strip())
            
            await self.db_manager.update_column(guild_id, discord_id, 'age', age)
            return True
        except ValueError:
            await ctx.send('Os valores inseridos são inválidos')
            return False
        
    async def change_gender(self, ctx, guild_id, discord_id):
        gender_message = await ctx.send('Por favor, informe seu gênero')
        for emoji in self.gender_emoji:
            await gender_message.add_reaction(emoji)
             
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in self.gender_emoji)
        gender = self.gender_emoji[str(reaction.emoji)]
      
        await self.db_manager.update_column(guild_id, discord_id, 'gender', gender)
        
        
    async def change_activity_level(self, ctx, guild_id, discord_id):
        await ctx.send('Escolha seu nível de atividade')
        
        message = await ctx.send(embed= await EmbedCreation.activity_embed(self.activity_levels))
        for emoji in self.activity_levels:
            await message.add_reaction(emoji)
        
        #o user é fornecido automaticamente pelo discord.py quando o evento é acionado  
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in self.activity_levels)
        activity_level = self.activity_levels[str(reaction.emoji)]

        await self.db_manager.update_column(guild_id, discord_id, 'activity_level', activity_level)
        
    
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserCommands(bot))
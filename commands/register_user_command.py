from discord.ext import commands
from data.database import DatabaseManager
from modules.fitness_calculator import FitnessCalculator
from modules.embeds import EmbedCreation
import discord


class RegisterUser(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db_manager = DatabaseManager()
        
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


    @commands.command(name='registrar', help='Faz o registro do usuário.')
    async def registrar(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.db_manager.create_table(guild_id)   
        
        #?Verifica se o usuário já está registrado no banco de dados
        discord_id = ctx.author.id
        existing_user = self.db_manager.get_user(guild_id, discord_id)
        
        
        if existing_user:
            await ctx.send('Você já está registrado.')
        else:
            try:
                await ctx.send('Por favor, digite seu peso em kg')
                weight_content = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
                # Strip() para remover os espaços em branco no começo e no fim da mensagem
                weight = weight_content.content.strip()
                if ',' in weight:
                    weight = weight.replace(',', '.')
                weight = float(weight)
                print(weight)


                await ctx.send('Por favor, digite sua altura em cm')
                height_content = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
                height = height_content.content.strip()
                # Caso o usuário tenha digitado a altura com vírgula
                if ',' in height:
                    height = height.replace(',', '')
                height = int(height)


                await ctx.send('Por favor, digite sua idade')
                age = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
                age = int(age.content.strip())

                
                gender_message = await ctx.send('Por favor, informe seu gênero')
                for emoji in self.gender_emoji:
                    await gender_message.add_reaction(emoji)     
                #o user é fornecido automaticamente pelo discord.py quando o evento é acionado 
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in self.gender_emoji)
                gender = self.gender_emoji[str(reaction.emoji)]
                
                
                await ctx.send('Escolha seu nível de atividade')
                message = await ctx.send(embed= await EmbedCreation.activity_embed(self.activity_levels))
                for emoji in self.activity_levels:
                    await message.add_reaction(emoji)
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=lambda reaction, user: user == ctx.author and str(reaction.emoji) in self.activity_levels)
                activity_level = self.activity_levels[str(reaction.emoji)]
                
                
                tdee = await FitnessCalculator.get_tdee(weight, height, age, gender, activity_level)
                
                
                #? Insere as informações do usuário no banco de dados
                self.db_manager.register_user(discord_id, guild_id, weight, height, age, gender, activity_level, tdee)
                await ctx.send('Registro concluído com sucesso.')
                await ctx.send(f"Use o comando $perfil para ver suas informações.")
            
            except TimeoutError:
                await ctx.send('Tempo esgotado. Por favor, tente novamente.')  
            except ValueError:
                await ctx.send('Valores inválidos. Tente novamente com valores válidos.')
            except discord.Forbidden:
                await ctx.send('Não tenho permissão para reagir a mensagem.')
               
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RegisterUser(bot))
import discord
from discord.ext import commands

class EmbedCreation:
    @staticmethod
    def create_nutrition_embed(food_name, calories, protein, fat, carbohydrates, serving_qty, serving_weight):
        '''CRIA O EMBED INFORMATIVO DOS MACROS DO ALIEMTNO'''
        embed = discord.Embed(
            title=f'Informações Nutricionais - {food_name}',
            description='Valores nutricionais do alimento',
            color=0x00ff00 
        )

        embed.add_field(name='Carboidratos', value=f"{carbohydrates} g", inline=True)
        embed.add_field(name='Proteína', value=f"{protein} g", inline=True)
        embed.add_field(name='Gordura', value=f"{fat} g", inline=True)
        embed.add_field(name='Calorias', value=f"{calories} kcal", inline=False)
        embed.add_field(name='Porção', value=f'{serving_qty} ({serving_weight}g)', inline=True)

        return embed
    
    @staticmethod
    def create_exercise_embed(calories, name, duration):
        embed = discord.Embed(
            title="Informação de exercício", 
            color=0xFF5733
            )

        embed.add_field(name="Exercício", value=name, inline=False)
        embed.add_field(name="Duração", value=f"{duration} Minutos", inline=False)
        embed.add_field(name="Calorias queimadas", value=f"{calories} Calorias", inline=False)

        return embed
    
    @staticmethod
    def create_user_embed(ctx, user_info):
        embed = discord.Embed(
            title=f"{ctx.author.name}",
            color=0x3498db,  
        )
        

        embed.set_thumbnail(url=ctx.author.avatar.url)
        weight, height, age, gender, activity_level, tdee = user_info[3:]

        embed.add_field(name="Peso", value=f"{weight} kg", inline=True)
        embed.add_field(name="Altura", value=f"{height} cm", inline=True)
        embed.add_field(name="Idade", value=f"{age} anos", inline=True)
        embed.add_field(name="Gênero", value=f"{gender}", inline=True)
        embed.add_field(name="Nível de Atividade", value=f"{activity_level}", inline=True)
        embed.add_field(name="TDEE", value=f"{tdee} calorias/dia", inline=True)

        return embed
    
    @staticmethod
    async def activity_embed(activity_levels_dict):        
        embed = discord.Embed(title=f'', color=0x696969)
        options = '\n'.join(f'{emoji} {activity}' for emoji, activity in activity_levels_dict.items())
        embed.add_field(name='', value=options, inline=False)
        
        return embed
    
    @staticmethod
    async def user_embed(user_infos_dict):
        embed = discord.Embed(title=f'', color=0x696969)
        options = '\n'.join(f'{emoji} {activity}' for emoji, activity in user_infos_dict.items())
        embed.add_field(name='', value=options, inline=False)
        
        return embed
    
    
        
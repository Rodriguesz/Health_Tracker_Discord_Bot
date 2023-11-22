from discord.ext import commands
from modules.embeds import EmbedCreation
from modules.fitness_calculator import FitnessCalculator
import discord

class FitnessCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.fitness_calculator = FitnessCalculator()
	

    @commands.command(name='macros', help='Calcula os macros dos alimentos consumidos.')
    async def macros(self, ctx: commands.Context, *, user_input: str = "") -> None:
        if user_input == "":
            await ctx.channel.send("Tente digitar $macros {nome do alimento} {quantidade em gramas ou porção}")
        else:
            food_list = self.fitness_calculator.getNutritionalInformation(user_input)
            # CASO A LISTA RETORNADA DE getNutritionalInformation SEJA VAZIA (A API NÃO ENCONTROU O ALIMENTO DIGITADO)
            if len(food_list) > 0:
                for food in range(len(food_list)):
                    await ctx.channel.send(
                        embed = EmbedCreation.create_nutrition_embed(
                            food_name= food_list[food]["food_name"].title(),
                            calories = food_list[food]["calories"],
                            protein= food_list[food]["protein"],
                            serving_qty= food_list[food]["serving_qty"],
                            carbohydrates= food_list[food]["total_carbohydrate"],
                            serving_weight= food_list[food]["serving_weight_grams"],
                            fat= food_list[food]["total_fat"]
                        )
                    )
            else:
                await ctx.channel.send("Ixi, não achei isso ai não piá.")
        
    
    @commands.command(name="kcal", help='Calcula as calorias gastas com os exercícios.')
    async def kcal(self, ctx: commands.Context, *, user_input: str = "") -> None: 
        if user_input == "":
            await ctx.channel.send("Tente digitar $kcal {exercício feito} {tempo feito}")
        else:
            exercise_list = self.fitness_calculator.getExerciseInformation(user_input)
            
            if len(exercise_list) > 0:
                for exercise in range(len(exercise_list)):
                    await ctx.channel.send(
                        embed = EmbedCreation.create_exercise_embed(
                            name= exercise_list[exercise]["name"].title(),
                            duration = exercise_list[exercise]["duration"],
                            calories= exercise_list[exercise]["calories"],
                            
                        )
                    )
            else:
                await ctx.channel.send("Não encontrei esse exercício ai não Zé. My bad minha :(")
                    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FitnessCommands(bot))
import requests
from googletrans import Translator
from decouple import config

API_KEY = config("NUTRITIONIX_API_KEY")
APP_ID = config("NUTRITIONIX_APP_ID")
HEADERS = {
            "x-app-id": APP_ID,
            "x-app-key": API_KEY,
        }


class FitnessCalculator:
    def __init__(self) -> None:
        self.translator = Translator()
    
    def getNutritionalInformation(self, food_eaten):
        food_eaten = self.translator.translate(food_eaten, dest='en').text
        body = {    
            "query": food_eaten,
        }

        response = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients", json=body, headers= HEADERS)
        data = response.json()
        
        
        #? PEGANDO OS DADOS QUE EU VOU USAR
        food_list = []
        if 'foods' in data:
            for food in range(len(data["foods"])):
                food_list.append(
                    {
                        "food_name":  str(self.translator.translate(data["foods"][food]["food_name"], dest="pt").text),
                        "serving_qty": data["foods"][food]["serving_qty"],
                        "serving_weight_grams": int(data["foods"][food]["serving_weight_grams"]),
                        "calories": int(data["foods"][food]["nf_calories"]),
                        "protein": int(data["foods"][food]["nf_protein"]),
                        "total_fat": int(data["foods"][food]["nf_total_fat"]),
                        "total_carbohydrate": int(data["foods"][food]["nf_total_carbohydrate"])
                    }
                )
        return food_list
    
    
    def getExerciseInformation(self, exercise):
        exercise = self.translator.translate(exercise, dest='en').text
        print(exercise)
        
        body = {    
            "query": exercise,
        }
        
        response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", json=body, headers= HEADERS)
        data = response.json()

        
        #? PEGANDO OS DADOS QUE EU VOU USAR
        exercise_list = []
        if 'exercises' in data:
            for exercise in range(len(data['exercises'])):
                exercise_list.append(
                    {
                        'name': self.translator.translate(data["exercises"][exercise]["name"], dest="pt").text,
                        'duration': int(data["exercises"][exercise]["duration_min"]),
                        'calories': int(data["exercises"][exercise]["nf_calories"]),
                    }
                )
        return exercise_list
    
    @staticmethod
    async def get_tdee(weight, height, age, gender, activity_level):
        if gender == 'Masculino':
            tmb = 88.362 + (13.397 * weight) + (4.799 * height) - (5.667 * age)
        elif gender == 'Feminino':
            tmb = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
        match activity_level:
            case 'Sedentário':
                tdee = tmb * 1.2
            case 'Leve':
                tdee = tmb * 1.375
            case 'Moderado':
                tdee = tmb * 1.55
            case 'Ativo':
                tdee = tmb * 1.725
            case 'Muito Ativo':
                tdee = tmb * 1.9
                
        return int(tdee) 
import sqlite3
from modules.fitness_calculator import FitnessCalculator

class DatabaseManager():
    def __init__(self):
        self.db_path = 'data/user_data.db'
    
    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def close_db(self, connection):
        connection.close()

    def create_table(self, guild_id):
        db = self.connect_db()
        cursor = db.cursor()

        # Cria tabela se não existir
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS users_{guild_id}(
                id INTEGER PRIMARY KEY,
                discord_id INTEGER,
                guild_id INTEGER,
                weight REAL,
                height INTEGER,
                age INTEGER,
                gender TEXT,
                activity_level TEXT,
                tdee INTEGER
            )
        ''')
        db.commit()
        self.close_db(db)
        
    def register_user(self, discord_id, guild_id, weight, height, age, gender, activity_level, tdee):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute(f'''
                    INSERT INTO users_{guild_id}(
                        discord_id, 
                        guild_id, 
                        weight, 
                        height, 
                        age, 
                        gender, 
                        activity_level, 
                        tdee)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (discord_id, guild_id, weight, height, age, gender, activity_level, tdee))

        print(f"Registering user: discord_id={discord_id}, guild_id={guild_id}, weight={weight}, height={height}, age={age}, gender={gender}, activity_level={activity_level}, tdee={tdee}")
        db.commit()
        self.close_db(db)

    def get_user(self, guild_id, discord_id):
        try:
            db = self.connect_db()
            cursor = db.cursor()

            # Seleciona o usuário na tabela específica do servidor
            cursor.execute(f'SELECT * FROM users_{guild_id} WHERE discord_id = ?', (discord_id,))
            user_info = cursor.fetchone()

            self.close_db(db)

            return user_info
        except sqlite3.Error as e:
            print(f"Erro ao obter informações do usuário: {e}")
            return None

    async def update_column(self, guild_id, discord_id, column_name, new_value):
        try:
            db = self.connect_db()
            cursor = db.cursor()

            # Atualiza o valor da coluna para o usuário com o ID especificado no servidor correspondente
            cursor.execute(f'''
                UPDATE users_{guild_id}
                SET {column_name} = ?
                WHERE discord_id = ?
            ''', (new_value, discord_id))
            db.commit()
            
            
            user = self.get_user(guild_id, discord_id)
            # '*' é usado para desempacotar os elementos da lista (vira um tupla)
            #[3:-1] pula os dois primeiros e o ultimo elento da lista
            tdee = await FitnessCalculator.get_tdee(*user[3:-1])
            
            cursor.execute(f'''
                UPDATE users_{guild_id}
                SET tdee = ?
                WHERE discord_id = ?
            ''', (tdee, discord_id))

            db.commit()
            self.close_db(db)

            print(f"A coluna '{column_name}' foi atualizada com sucesso para o usuário com ID {discord_id}")
        except sqlite3.Error as e:
            print(f"Erro na atualização da coluna '{column_name}': {e}")

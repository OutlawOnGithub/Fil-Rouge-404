import asyncpg
import random
import time

class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None
    
    async def connect(self):
        """Établit la connexion à la base de données"""
        self.pool = await asyncpg.create_pool(
            host=self.config['host'],
            port=self.config['port'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password']
        )
        print("Connexion à la base de données établie")
    
    async def get_user(self, user_id):
        """Récupère les données d'un utilisateur"""
        async with self.pool.acquire() as conn:
            query = f"SELECT * FROM {self.config['schema']}.server WHERE userId = $1"
            return await conn.fetchrow(query, user_id)
    
    async def create_user(self, user_id):
        """Crée un nouvel utilisateur dans la base"""
        async with self.pool.acquire() as conn:
            query = f"""
                INSERT INTO {self.config['schema']}.server (userId, balance, objects, lastPull)
                VALUES ($1, 0, '', 0)
                ON CONFLICT (userId) DO NOTHING
            """
            await conn.execute(query, user_id)
    
    async def get_balance(self, user_id):
        """Récupère la balance d'un utilisateur"""
        user = await self.get_user(user_id)
        if not user:
            await self.create_user(user_id)
            return 0
        return user['balance']
    
    async def update_balance(self, user_id, amount):
        """Met à jour la balance d'un utilisateur"""
        async with self.pool.acquire() as conn:
            query = f"""
                UPDATE {self.config['schema']}.server
                SET balance = balance + $2
                WHERE userId = $1
            """
            await conn.execute(query, user_id, amount)
    
    async def add_beurre(self, user_id):
        """Ajoute un montant aléatoire de beurre (2-20) à l'utilisateur"""
        user = await self.get_user(user_id)
        if not user:
            await self.create_user(user_id)
        
        amount = random.randint(2, 20)
        await self.update_balance(user_id, amount)
        return amount
    
    async def add_object(self, user_id, obj):
        """Ajoute un objet à la collection de l'utilisateur"""
        user = await self.get_user(user_id)
        if not user:
            await self.create_user(user_id)
            current_objects = ""
        else:
            current_objects = user['objects'] or ""
        
        # Ajoute l'objet à la liste (séparés par des virgules)
        if current_objects:
            new_objects = f"{current_objects},{obj}"
        else:
            new_objects = obj
        
        async with self.pool.acquire() as conn:
            query = f"""
                UPDATE {self.config['schema']}.server
                SET objects = $2
                WHERE userId = $1
            """
            await conn.execute(query, user_id, new_objects)
    
    async def pull_object(self, user_id):
        """Effectue un pull d'objet si l'utilisateur a assez de beurre"""
        PULL_COST = 10
        OBJECTS = ['bout de bois', 'crotte', 'lingot']
        WEIGHTS = [50, 35, 15]  # Probabilités : bois (50%), crotte (35%), lingot (15%)
        
        user = await self.get_user(user_id)
        if not user:
            await self.create_user(user_id)
            return {
                'error': True,
                'message': "Tu n'as pas assez de beurre ! Utilise !beurre pour en obtenir."
            }
        
        balance = user['balance']
        
        if balance < PULL_COST:
            return {
                'error': True,
                'message': f"Tu n'as pas assez de beurre ! Il te faut {PULL_COST} beurres (tu en as {balance})."
            }
        
        # Tire un objet au sort
        obj = random.choices(OBJECTS, weights=WEIGHTS, k=1)[0]
        
        # Met à jour la base de données
        await self.update_balance(user_id, -PULL_COST)
        await self.add_object(user_id, obj)
        
        # Met à jour lastPull
        current_time = int(time.time())
        async with self.pool.acquire() as conn:
            query = f"""
                UPDATE {self.config['schema']}.server
                SET lastPull = $2
                WHERE userId = $1
            """
            await conn.execute(query, user_id, current_time)
        
        return {
            'error': False,
            'object': obj,
            'cost': PULL_COST,
            'new_balance': balance - PULL_COST
        }
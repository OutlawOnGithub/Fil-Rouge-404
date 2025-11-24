import asyncpg
import json
import time

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: asyncpg.pool.Pool = None

    # --------------------------
    # Connexion à la DB
    # --------------------------
    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        async with self.pool.acquire() as conn:
            # Crée la table users si elle n'existe pas
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    balance INT NOT NULL DEFAULT 0,
                    objects JSONB NOT NULL DEFAULT '[]',
                    lastPull BIGINT NOT NULL DEFAULT 0
                );
            """)
        print("✅ Users table ensured in DB.")

    # --------------------------
    # Utilitaires pour joueurs
    # --------------------------

    async def add_user_if_not_exists(self, user_id: int):
        """Ajoute un utilisateur si il n'existe pas encore."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users(id)
                VALUES($1)
                ON CONFLICT(id) DO NOTHING
            """, user_id)

    async def get_user(self, user_id: int):
        """Récupère les informations d'un utilisateur."""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE id=$1", user_id)

    async def update_balance(self, user_id: int, amount: int):
        """Ajoute ou retire de l'argent à l'utilisateur."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE users
                SET balance = balance + $1
                WHERE id=$2
            """, amount, user_id)

    async def set_balance(self, user_id: int, amount: int):
        """Définit le solde exact de l'utilisateur."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE users
                SET balance = $1
                WHERE id=$2
            """, amount, user_id)

    async def update_last_pull(self, user_id: int, timestamp: int = None):
        """Met à jour la date du dernier pull."""
        if timestamp is None:
            timestamp = int(time.time())
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE users
                SET lastPull=$1
                WHERE id=$2
            """, timestamp, user_id)

    async def add_object(self, user_id: int, obj: str):
        """Ajoute un objet à la liste de l'utilisateur."""
        async with self.pool.acquire() as conn:
            # Récupère la liste actuelle
            row = await conn.fetchrow("SELECT objects FROM users WHERE id=$1", user_id)
            objects = row['objects'] if row else []
            if not isinstance(objects, list):
                objects = []
            objects.append(obj)
            # Met à jour la DB
            await conn.execute("""
                UPDATE users
                SET objects = $1::jsonb
                WHERE id=$2
            """, json.dumps(objects), user_id)

    async def get_objects(self, user_id: int):
        """Récupère la liste des objets d'un utilisateur."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT objects FROM users WHERE id=$1", user_id)
            if row:
                return row['objects']
            return []

    async def can_pull(self, user_id: int, cooldown: int):
        """Vérifie si l'utilisateur peut pull selon lastPull + cooldown."""
        user = await self.get_user(user_id)
        if not user:
            return True
        last_pull = user['lastpull']  # timestamp EPOCH
        now = int(time.time())
        return now - last_pull >= cooldown

import asyncpg
import asyncio
import json

class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        # Crée la table si elle n'existe pas
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    balance INT NOT NULL DEFAULT 0,
                    objects JSONB NOT NULL DEFAULT '[]',
                    lastPull BIGINT NOT NULL DEFAULT 0
                );
            """)

    # --------------------------
    #  Utilitaires joueurs
    # --------------------------
    async def add_user_if_not_exists(self, user_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users(id)
                VALUES($1)
                ON CONFLICT(id) DO NOTHING
            """, user_id)

    async def get_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE id=$1", user_id)

    async def update_balance(self, user_id: int, amount: int):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET balance = balance + $1 WHERE id=$2", amount, user_id)

    async def update_last_pull(self, user_id: int, timestamp: int):
        async with self.pool.acquire() as conn:
            await conn.execute("UPDATE users SET lastPull=$1 WHERE id=$2", timestamp, user_id)

    async def add_object(self, user_id: int, obj: str):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE users
                SET objects = objects || $1::jsonb
                WHERE id=$2
            """, json.dumps([obj]), user_id)

import aiosqlite
from data.config import DB


async def exists(user_id: int = None, user_name: str = None) -> bool:
    async with aiosqlite.connect(DB) as conn:
        if user_id is not None:
            query = "SELECT id FROM user_list WHERE id = ?"
            param = user_id
        else:
            query = "SELECT name FROM user_list WHERE name = ?"
            param = user_name
        cursor: aiosqlite.Cursor
        async with conn.execute(query, (param,)) as cursor:
            result = await cursor.fetchone()
            if result is None:
                return False
    return True


async def insert_user(user_id: int, user_name: str,) -> None:
    async with aiosqlite.connect(DB) as conn:
        query = "INSERT INTO user_list(id, name) VALUES(?, ?)"
        await conn.execute(query, (user_id, user_name))
        await conn.commit()


async def others_present() -> bool:
    async with aiosqlite.connect(DB) as conn:
        query = "SELECT * FROM user_list"
        cursor: aiosqlite.Cursor
        async with conn.execute(query) as cursor:
            user_list = await cursor.fetchall()
    if len(user_list) > 1:
        return True
    return False

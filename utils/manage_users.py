from sqlalchemy import text
from db.database import sqlite_engine


# Получаем id Пользователей
def get_users() -> list:
    with sqlite_engine.connect() as conn:
        res = conn.execute(text(f'SELECT telegram_id FROM users WHERE id > 0'))
        users = res.all()

    return [user[0] for user in users]
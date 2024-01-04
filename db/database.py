import sqlite3
import mysql.connector
from loguru import logger
import asyncio

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from db.db_config import settings


sqlite_engine = create_engine(
    url=settings.DATABASE_URL_sqlite,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)

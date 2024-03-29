
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database/fastcrudapp.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, future=True, echo=True
    )
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
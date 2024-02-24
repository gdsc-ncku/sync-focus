from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from setting.config import get_settings

settings = get_settings()

# Create engine
engine = create_async_engine(settings.database_url, echo=True)

# Create session
async_session = sessionmaker(
    engine, expire_on_commit=False, autocommit=False, class_=AsyncSession
)

Base = declarative_base()

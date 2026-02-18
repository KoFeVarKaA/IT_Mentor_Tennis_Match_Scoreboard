from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import config

sync_engine = create_engine(
    url=config.settings.DATABASE_URL_mysqlclient,
    echo=True,  
    pool_size=5, 
    max_overflow=10  
)

session_factory = sessionmaker(bind=sync_engine)

class Base(DeclarativeBase):
    pass
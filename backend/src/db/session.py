from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings


def get_db_session():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        connect_args={"TrustServerCertificate": "Yes"},
        pool_pre_ping=True,
        pool_size=35,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"TrustServerCertificate": "Yes"},
    pool_pre_ping=True,
    pool_size=35,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

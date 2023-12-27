from sqlalchemy import NVARCHAR, Column, Integer

from src.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(NVARCHAR(500), nullable=True)
    wallet_address = Column(NVARCHAR(500), nullable=True)

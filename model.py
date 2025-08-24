from sqlalchemy import Column, Enum, Integer, String, Boolean
from database import Base
from schemas import UserRole

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    Lastname = Column(String, unique=True, index=True, nullable=False)
    Othername = Column(String, unique=True, index=True, nullable=False)
    Phonenumber = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role =  Column(Enum(UserRole), default=UserRole.buyer, nullable=False)

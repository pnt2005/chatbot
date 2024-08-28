from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)

class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)


from sqlalchemy import Column, String, Integer, Enum, DateTime
from datetime import datetime, timedelta
from db import Base

class User(Base):
    __tablename__ = 'users'
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False,primary_key=True)
    password = Column(String(255), nullable=False)    
class Room(Base):
    __tablename__ = 'rooms'
    roomid = Column(Integer, nullable=False, primary_key=True)
    location = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Enum('booked', 'vacant', name='enum_options'), nullable=False)

class Booked(Base):
    __tablename__ = 'booked'
    useremail = Column(String(30), nullable=False, primary_key=True)
    payment = Column(Enum('paid', 'unpaid', name='payment_status'), nullable=False, default='unpaid')
    check_out = Column(DateTime, nullable=False, primary_key=True, default=lambda: datetime.utcnow() + timedelta(hours=12))


from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    email = Column(String, nullable=False)
    points = Column(Integer, nullable=False, default=0)
    next_milestone = Column(Integer, nullable=False, default=10)

    bookings = relationship("Booking")


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    email = Column(String, nullable=False)
    webhook = Column(String)

    bookings = relationship("Booking")


class Promotion(Base):
    __tablename__ = "promotion"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires = Column(DateTime, nullable=False, default=datetime.utcnow)


class Voucher(Base):
    __tablename__ = "voucher"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    used_for = Column(Integer)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires = Column(DateTime, nullable=False, default=datetime.utcnow)


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    date_time = Column(DateTime, nullable=False)
    party_size = Column(Integer, nullable=False)

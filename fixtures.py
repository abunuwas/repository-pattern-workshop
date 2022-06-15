import os
from datetime import timedelta, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_access.models import User, Restaurant, Promotion, Voucher, Booking

session_maker = sessionmaker(bind=create_engine(os.getenv("DB_URL")))

restaurant = Restaurant(
    name="Super Duper Restaurant",
    email="restaurant@example.com",
    webhook="http://localhost:3000/webhook",
)

user = User(email="user@example.com")

with session_maker() as session:
    session.add(restaurant)
    session.add(user)
    session.commit()

with session_maker() as session:
    restaurant = session.query(Restaurant).first()
    user = session.query(Restaurant).first()
    promotion = Promotion(restaurant_id=restaurant.id, expires=datetime.utcnow() + timedelta(days=1))
    session.add(promotion)
    session.commit()

with session_maker() as session:
    restaurant = session.query(Restaurant).first()
    promotion = session.query(Promotion).filter(Promotion.restaurant_id == restaurant.id, Promotion.expires > datetime.utcnow()).first()
    session.commit()

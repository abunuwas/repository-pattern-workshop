from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class Restaurant(BaseModel):
    id: int
    name: str
    created: datetime
    email: str
    webhook: str


class Promotion(BaseModel):
    id: int
    restaurant_id: int
    created: datetime
    expires: datetime


class User(BaseModel):
    id: int
    created: datetime
    email: str
    points: int
    next_milestone: int


class Voucher(BaseModel):
    id: int
    user_id: int
    used_for: Optional[int]
    created: datetime
    expires: datetime


class Booking(BaseModel):
    id: int
    created: datetime
    user_id: int
    restaurant_id: int
    date_time: datetime
    party_size: int


class DummyRestaurantRepository:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        restaurant = Restaurant(
            id=1, name='Restaurant', created=datetime.utcnow(), email='restaurant@example.com', webhook='http://localhost:3000/webhook'
        )
        promotion = Promotion(
            id=1, restaurant_id=1, created=datetime.utcnow(), expires=datetime.utcnow() + timedelta(days=1)
        )
        return restaurant, promotion


class DummyUserRepository:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, id_):
        user = User(
            id=1, created=datetime.utcnow(), email="user@example.com", points=0, next_milestone=10
        )
        active_vouchers = Voucher(id=1, user_id=1, created=datetime.utcnow(), expires=datetime.utcnow() + timedelta(days=1))
        return user, active_vouchers

    def update(self, id_, **kwargs):
        user, _ = self.get(id_)
        for key, value in kwargs.items():
            setattr(user, key, value)


class DummyBookingsRepository:
    def __init__(self, *args, **kwargs):
        pass

    def add(self, user_id: int, restaurant_id: int, date_time: datetime, party_size: int):
        booking = Booking(
            id=1,
            created=datetime.utcnow(),
            user_id=user_id,
            restaurant_id=restaurant_id,
            date_time=date_time,
            party_size=party_size,
        )
        return booking


class DummyVoucherRepository:
    def __init__(self, *args, **kwargs):
        pass

    def get(self, **_):
        return Voucher(id=1, user_id=1, created=datetime.utcnow(), expires=datetime.utcnow() + timedelta(days=1))

    def add(self, user_id: int, expires: datetime):
        return Voucher(id=1, user_id=user_id, created=datetime.utcnow(), expires=expires)

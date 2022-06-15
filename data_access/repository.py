from datetime import datetime

from data_access.models import Restaurant, User, Booking, Promotion, Voucher


class RestaurantRepository:
    def __init__(self, session):
        self.session = session

    def get(self, id_):
        restaurant = self.session.query(Restaurant).filter(Restaurant.id == id_).first()
        promotion = self.session.query(Promotion).filter(
                Promotion.restaurant_id == restaurant.id, Promotion.expires > datetime.utcnow()
        ).first()
        return restaurant, promotion


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get(self, id_):
        user = self.session.query(User).filter(User.id == id_).first()
        active_vouchers = self.session.query(Voucher).filter(Voucher.user_id == id_, Voucher.expires > datetime.utcnow()).count()
        return user, active_vouchers

    def update(self, id_, **kwargs):
        user, _ = self.get(id_)
        for key, value in kwargs.items():
            setattr(user, key, value)


class BookingsRepository:
    def __init__(self, session):
        self.session = session

    def add(self, user_id: int, restaurant_id: int, date_time: datetime, party_size: int):
        booking = Booking(
            user_id=user_id,
            restaurant_id=restaurant_id,
            date_time=date_time,
            party_size=party_size,
        )
        self.session.add(booking)
        return booking


class VoucherRepository:
    def __init__(self, session):
        self.session = session

    def get(self, **filters):
        return self.session.query(Voucher).filter_by(**filters).first()

    def add(self, user_id: int, expires: datetime):
        voucher = Voucher(user_id=user_id, expires=expires)
        self.session.add(voucher)
        return voucher

from datetime import datetime, timedelta

from fastapi import APIRouter
from pydantic import BaseModel, conint
from starlette import status
from starlette.requests import Request

from data_access.models import User, Restaurant, Booking, Promotion, Voucher

router = APIRouter()


class BookTable(BaseModel):
    restaurant: int = 1
    party_size: conint(ge=1)
    date_time: datetime


class BookingConfirmation(BaseModel):
    booking_id: int
    restaurant: str
    party_size: int
    date_time: datetime
    voucher: int


@router.post("/bookings", status_code=status.HTTP_201_CREATED, response_model=BookingConfirmation)
def book_table(request: Request, booking_details: BookTable):
    with request.app.session_maker() as session:
        user = session.query(User).filter(User.id == 1).first()
        restaurant = session.query(Restaurant).filter(Restaurant.id == booking_details.restaurant).first()
        booking = Booking(
                user_id=user.id,
                restaurant_id=restaurant.id,
                date_time=booking_details.date_time,
                party_size=booking_details.party_size,
            )
        session.add(booking)
        if session.query(Promotion).filter(
                Promotion.restaurant_id == restaurant.id, Promotion.expires > datetime.utcnow()
        ).first():
            user.points += 10
        else:
            user.points += 1
        if user.next_milestone == user.points:
            new_voucher = Voucher(user_id=user.id, expires=datetime.utcnow() + timedelta(days=7))
            session.add(new_voucher)
            user.next_milestone += 10
        session.commit()
        return {
            "booking_id": booking.id,
            "restaurant": restaurant.name,
            "party_size": booking.party_size,
            "date_time": booking.date_time,
            "voucher": new_voucher.id if new_voucher else None
        }
    # create booking record
    # we update user's record with their preferences
    # notify restaurant's API


@router.get("/me")
def get_user(request: Request):
    with request.app.session_maker() as session:
        user = session.query(User).first()
        active_vouchers = session.query(Voucher).filter(Voucher.user_id == user.id, Voucher.expires > datetime.utcnow()).all()
        return {
            "id": user.id,
            "email": user.email,
            "points": user.points,
            "next_milestone": user.next_milestone,
            "active_vouchers": len(active_vouchers)
        }

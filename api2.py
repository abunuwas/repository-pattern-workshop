from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, conint
from starlette import status
from starlette.requests import Request

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
    new_voucher: Optional[int]


@router.post("/bookings", status_code=status.HTTP_201_CREATED, response_model=BookingConfirmation)
def book_table(request: Request, booking_details: BookTable):
    with request.app.session_maker() as session:
        user_repo = request.app.repositories_registry.user_repository(session)
        restaurant_repo = request.app.repositories_registry.restaurant_repository(session)
        bookings_repo = request.app.repositories_registry.bookings_repository(session)
        voucher_repo = request.app.repositories_registry.voucher_repo(session)

        user_id = 1

        booking = bookings_repo.add(
            user_id=user_id,
            restaurant_id=booking_details.restaurant,
            date_time=booking_details.date_time,
            party_size=booking_details.party_size,
        )

        user, _ = user_repo.get(user_id)
        restaurant, promotion = restaurant_repo.get(booking_details.restaurant)
        if promotion:
            user.points += 10
        else:
            user.points += 1
        if user.next_milestone == user.points:
            new_voucher = voucher_repo.add(user_id=user_id, expires=datetime.utcnow() + timedelta(days=7))
            user.next_milestone += 10
        else:
            new_voucher = None

        session.commit()

        return {
            "booking_id": booking.id,
            "restaurant": restaurant.name,
            "party_size": booking.party_size,
            "date_time": booking.date_time,
            "new_voucher": new_voucher.id if new_voucher else None,
        }

    # create booking record
    # we update user's record with their preferences
    # notify restaurant's API


@router.get("/me")
def get_user(request: Request):
    with request.app.session_maker() as session:
        user_repo = request.app.repositories_registry.user_repository(session)

        user, active_vouchers = user_repo.get(1)

        return {
            "id": user.id,
            "email": user.email,
            "points": user.points,
            "next_milestone": user.next_milestone,
            "active_vouchers": active_vouchers
        }

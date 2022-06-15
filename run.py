import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_access.repositories_registry import RepositoriesRegistry
from data_access.repository import BookingsRepository, RestaurantRepository, UserRepository, VoucherRepository
from server import create_server

session_maker = sessionmaker(bind=create_engine(os.getenv("DB_URL")))

repositories_registry = RepositoriesRegistry(
    bookings_repository=BookingsRepository,
    restaurant_repository=RestaurantRepository,
    user_repository=UserRepository,
    voucher_repository=VoucherRepository,
)

server = create_server(repositories_registry=repositories_registry, session_maker=session_maker)

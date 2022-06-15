from unittest.mock import MagicMock

from starlette.testclient import TestClient

from data_access.repositories_registry import RepositoriesRegistry
from dummy_repositories import DummyVoucherRepository, DummyUserRepository, DummyRestaurantRepository, \
    DummyBookingsRepository
from server import create_server

server = create_server(
    repositories_registry=RepositoriesRegistry(
        bookings_repository=DummyBookingsRepository,
        restaurant_repository=DummyRestaurantRepository,
        user_repository=DummyUserRepository,
        voucher_repository=DummyVoucherRepository,
    ),
    session_maker=MagicMock(),
)

test_client = TestClient(app=server)


def test():
    payload = {
        "restaurant": 1,
        "party_size": 1,
        "date_time": "2022-07-14T17:02:01.373Z"
    }
    response = test_client.post('/bookings', json=payload)
    assert response.status_code == 201
    assert response.json()['voucher'] is not None

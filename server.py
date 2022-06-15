from fastapi import FastAPI

from api2 import router


def create_server(repositories_registry=None, session_maker=None):
    server = FastAPI(debug=True)
    server.include_router(router)
    server.repositories_registry = repositories_registry
    server.session_maker = session_maker
    return server

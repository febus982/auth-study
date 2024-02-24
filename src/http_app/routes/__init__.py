from fastapi import FastAPI

from http_app.routes import hello, ping


def init_routes(app: FastAPI) -> None:
    app.include_router(ping.router)
    app.include_router(hello.router)

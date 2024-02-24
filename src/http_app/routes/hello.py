import logging
from typing import Annotated

from joserfc import jwt, jwk
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient

from http_app.templates import templates

router = APIRouter(prefix="/hello")

# Not part of this PoC, we should use a TTL cache here (i.e. 1H)
async def get_jwks() -> jwk.KeySet:
    async with AsyncClient() as ac:
        response = await ac.get("http://oathkeeper:4456/.well-known/jwks.json")
        response.raise_for_status()

    return jwk.KeySet.import_key_set(response.json())


async def get_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    jwks: Annotated[jwk.KeySet, Depends(get_jwks)],
) -> jwt.Token:
    return jwt.decode(
        value=credentials.credentials,
        key=jwks,
    )


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def hello(
    request: Request,
    jwt_token: Annotated[jwt.Token, Depends(get_token)]
):
    logging.info(jwt_token.header)
    logging.info(jwt_token.claims)

    async with AsyncClient() as ac:
        response = await ac.get(
            "http://127.0.0.1:8000/hello/new",
            headers={"Authorization": request.headers["Authorization"]}
        )
        response.raise_for_status()

    return templates.TemplateResponse("hello.html", {"request": request})


@router.get("/new", response_class=HTMLResponse, include_in_schema=False)
async def hello_new(
    request: Request,
    jwt_token: Annotated[jwt.Token, Depends(get_token)]
):

    logging.info("CALLED NEW")
    logging.info(jwt_token.header)
    logging.info(jwt_token.claims)

    return templates.TemplateResponse("hello.html", {"request": request})

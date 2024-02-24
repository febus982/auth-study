import logging
from typing import Annotated

from joserfc import jwt, jwk
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import AsyncClient

from http_app.templates import templates

router = APIRouter(prefix="/hello")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def hello(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
):
    async with AsyncClient() as ac:
        response = await ac.get("http://oathkeeper:4456/.well-known/jwks.json")
        response.raise_for_status()

    jwks = jwk.KeySet.import_key_set(response.json())

    token = jwt.decode(
        value=credentials.credentials,
        key=jwks,
    )
    logging.info(token.header)
    logging.info(token.claims)

    return templates.TemplateResponse("hello.html", {"request": request})

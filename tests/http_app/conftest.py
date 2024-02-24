import pytest
from fastapi import FastAPI
from http_app import create_app


@pytest.fixture(scope="function")
def testapp(test_config) -> FastAPI:
    return create_app(test_config=test_config)

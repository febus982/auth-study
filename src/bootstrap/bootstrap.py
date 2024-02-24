from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Object
from pydantic import BaseModel, ConfigDict

from .config import AppConfig
from .di_container import Container
from .logs import init_logger


class InitReference(BaseModel):
    di_container: DynamicContainer

    model_config = ConfigDict(arbitrary_types_allowed=True)


def application_init(app_config: AppConfig) -> InitReference:
    container = Container(
        config=Object(app_config),
    )
    init_logger(app_config)

    return InitReference(
        di_container=container,
    )

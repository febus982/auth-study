from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Dependency

from bootstrap.config import AppConfig


class Container(DeclarativeContainer):
    """
    Dependency injection container.

    Docs: https://python-dependency-injector.ets-labs.org/
    """

    wiring_config = WiringConfiguration(
        packages=[
            "bootstrap",
        ]
    )

    """
    We could use the config provider but it would transform our nice typed
    configuration in a dictionary, therefore we return it as a raw object.
    """
    config = Dependency(instance_of=AppConfig)

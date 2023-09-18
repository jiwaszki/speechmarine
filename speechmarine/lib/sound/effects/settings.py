from abc import ABC, abstractmethod
from typing import Any


# TODO: should Preset call be a specific effect Setttings class?
class Settings(ABC):
    """Base class for effect settings."""

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize settings."""
        pass

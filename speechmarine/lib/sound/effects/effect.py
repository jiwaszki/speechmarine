from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

from speechmarine.lib.sound.effects.settings import Settings

T = TypeVar("T", bound="Settings")


class Effect(ABC, Generic[T]):
    """Base class for the effect."""

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the Effect class with the given settings.

        Args:
            *args (Any): Additional positional arguments specific to the effect.
            **kwargs (Any): Additional keyword arguments specific to the effect.
        """
        self._settings = None

    @property
    def settings(self) -> T:
        """Return the settings of the effect.

        Returns:
            T: An instance of a Settings subclass.
        """
        return self._settings

    @abstractmethod
    def apply(self, audio_data, sampling_rate) -> Any:
        """Modify the input audio data and return the modified data.

        Args:
            TODO

        Returns:
            Any: The modified audio data.
        """
        pass

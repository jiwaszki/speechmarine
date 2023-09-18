import numpy as np

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


class NormalizerSettings(Settings):
    def __init__(self) -> None:
        pass


class Normalizer(Effect[NormalizerSettings]):
    """Adds echo on the top of the original data."""

    def __init__(self) -> None:
        self._settings = NormalizerSettings()

    def apply(self, audio_data, sampling_rate=None):
        return audio_data / np.max(np.abs(audio_data))

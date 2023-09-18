import numpy as np
from scipy.signal import lfilter

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


class EchoSettings(Settings):
    def __init__(self, delay, feedback, attenuation) -> None:
        self._delay = delay
        self._feedback = feedback
        self._attenuation = attenuation

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @property
    def feedback(self):
        return self._delay

    @feedback.setter
    def feedback(self, value):
        self._feedback = value

    @property
    def attenuation(self):
        return self._attenuation

    @attenuation.setter
    def attenuation(self, value):
        self._attenuation = value


class Echo(Effect[EchoSettings]):
    """Adds echo on the top of the original data."""

    def __init__(self, delay, feedback, attenuation) -> None:
        self._settings = EchoSettings(delay, feedback, attenuation)

    # TODO: how to ommit sampling_rate here as it is unused?
    def apply(self, audio_data, sampling_rate=None):
        # TODO: add equalization from the beinging of the tutorial
        echo_filter = np.zeros(self.settings.delay + 1)
        echo_filter[0] = 1
        echo_filter[-1] = self.settings.attenuation
        return (audio_data * self.settings.feedback) + lfilter(
            echo_filter, 1, audio_data
        )

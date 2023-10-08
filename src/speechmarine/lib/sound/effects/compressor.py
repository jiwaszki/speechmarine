import numpy as np
from librosa import db_to_amplitude

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings
from speechmarine._speechmarine_impl import gain_reduction_loop


class CompressorSettings(Settings):
    def __init__(self, threshold, ratio, attack, release, gain) -> None:
        self._threshold = threshold
        self._ratio = ratio
        self._attack = attack
        self._release = release
        self._gain = gain

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        self._ratio = value

    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def release(self):
        return self._release

    @release.setter
    def release(self, value):
        self._attack = value

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value


class Compressor(Effect[CompressorSettings]):
    """TODO"""

    def __init__(self, threshold, ratio, attack, release, gain) -> None:
        self._settings = CompressorSettings(threshold, ratio, attack, release, gain)

    def apply(self, audio_data, sampling_rate):
        # Convert threshold from dB to linear
        threshold = db_to_amplitude(self.settings.threshold)
        # Calculate the envelope of the audio data
        envelope = np.abs(audio_data)
        # Smooth the envelope using an attack-release filter
        attack_time = self.settings.attack / 1000  # Convert attack time to seconds
        release_time = self.settings.release / 1000  # Convert release time to seconds
        alpha_attack = np.exp(-1 / (sampling_rate * attack_time))
        alpha_release = np.exp(-1 / (sampling_rate * release_time))

        gain_reduction = np.zeros_like(envelope)
        smoothed_envelope = np.zeros_like(envelope)

        gain_reduction = gain_reduction_loop(
            gain_reduction,
            envelope,
            smoothed_envelope,
            self.settings.ratio,
            threshold,
            alpha_attack,
            alpha_release,
        )

        # Apply gain reduction to the audio data
        compressed_audio_data = audio_data * gain_reduction
        return compressed_audio_data * db_to_amplitude(self.settings.gain)

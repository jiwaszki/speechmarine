import numpy as np

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


class ReverbSettings(Settings):
    def __init__(self, dry, wet, wide) -> None:
        self._dry = dry
        self._wet = wet
        self._wide = wide

    @property
    def dry(self):
        return self._dry

    @dry.setter
    def dry(self, value):
        self._dry = value

    @property
    def wet(self):
        return self._wet

    @wet.setter
    def wet(self, value):
        self._wet = value

    @property
    def wide(self):
        return self._wide

    @wide.setter
    def wide(self, value):
        self._wide = value


class Reverb(Effect[ReverbSettings]):
    """TODO"""

    def __init__(self, dry, wet, wide) -> None:
        self._settings = ReverbSettings(dry, wet, wide)

    def apply(self, audio_data, sampling_rate):
        # Convolve the audio data with the impulse response
        convolved_audio = np.convolve(
            audio_data, self._synthesize_impulse_response(sampling_rate)
        )
        # Normalize the convolved audio
        convolved_audio /= np.max(np.abs(convolved_audio), axis=0)
        # Mix the dry and wet signals
        return (
            self.settings.dry * audio_data
            + self.settings.wet * convolved_audio[: len(audio_data)]
        )

    def _synthesize_impulse_response(self, sampling_rate):
        decay_samples = int(self.settings.wide * sampling_rate)
        time = np.linspace(0, self.settings.wide, decay_samples, endpoint=False)
        # Exponential decay model
        decay_curve = np.exp(-5 * time)
        # Randomize phase for a more diffuse sound
        random_phase = np.exp(1j * np.random.uniform(0, 2 * np.pi, decay_samples))
        # Convert the decay curve to the frequency domain
        decay_spectrum = np.fft.fft(decay_curve * random_phase)
        # Convert the decay spectrum back to the time domain
        impulse_response = np.real(np.fft.ifft(decay_spectrum))
        return impulse_response

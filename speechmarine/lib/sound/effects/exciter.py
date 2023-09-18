import numpy as np
import librosa
from scipy.signal import butter, filtfilt

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


class ExciterSettings(Settings):
    def __init__(self, cutoff, order, gain) -> None:
        self._cutoff = cutoff
        self._order = order
        self._gain = gain

    @property
    def cutoff(self):
        return self._cutoff

    @cutoff.setter
    def cutoff(self, value):
        self._cutoff = value

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, value):
        self._gain = value


class Exciter(Effect[ExciterSettings]):
    """TODO"""

    def __init__(self, cutoff, order, gain) -> None:
        self._settings = ExciterSettings(cutoff, order, gain)

    def apply(self, audio_data, sampling_rate):
        # Create a high-pass filter
        b, a = self._create_filter(sampling_rate)
        # Apply the high-pass filter to the audio data
        filtered_audio = filtfilt(b, a, audio_data)
        # Apply harmonic generation by squaring the filtered audio
        harmonics = filtered_audio * filtered_audio
        # Normalize harmonics
        harmonics /= np.max(np.abs(harmonics))
        # Mix the harmonics back with the original audio data
        excited_audio = (
            audio_data + librosa.db_to_amplitude(self.settings.gain) * harmonics
        )
        # Normalize the output audio
        excited_audio /= np.max(np.abs(excited_audio))
        return excited_audio

    def _create_filter(self, sampling_rate):
        nyq = 0.5 * sampling_rate
        normalized_cutoff = self.settings.cutoff / nyq
        b, a = butter(self.settings.order, normalized_cutoff, btype="high")
        return b, a

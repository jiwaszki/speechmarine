import numpy as np
import librosa
from scipy.signal import butter, sosfilt

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


class BandpassSettings(Settings):
    def __init__(self, bands, num_bands, order, gain) -> None:
        self._bands = bands  # TODO: rename, it means gain on different bands
        self._num_bands = num_bands
        self._order = order
        self._gain = gain

    @property
    def bands(self):
        return self._bands

    @bands.setter
    def bands(self, value):
        self._bands = value

    @property
    def num_bands(self):
        return self._num_bands

    @num_bands.setter
    def num_bands(self, value):
        self._num_bands = value

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


class Bandpass(Effect[BandpassSettings]):
    """TODO"""

    def __init__(self, bands, num_bands, order, gain) -> None:
        self._settings = BandpassSettings(bands, num_bands, order, gain)

    def apply(self, audio_data, sampling_rate):
        # TODO: make better bands to reflect DAWs
        min_freq = 31.0  # TODO: what <31 k means?
        max_freq = 25000.0  # TODO: what > 25k Hz means?
        bands = np.geomspace(min_freq, max_freq, num=self.settings.num_bands + 1)
        filtered_audio = np.zeros_like(audio_data)
        for i in range(self.settings.num_bands):
            sos = self._create_filter(bands[i], bands[i + 1], sampling_rate)
            filtered_band = self._apply_filter(audio_data, sos)
            filtered_audio += filtered_band * librosa.db_to_amplitude(
                self.settings.bands[i]
            )  # apply gain
        return filtered_audio * librosa.db_to_amplitude(
            self.settings.gain
        )  # apply overall gain at the end

    def _create_filter(self, lowcut, highcut, sampling_rate):
        nyq = 0.5 * sampling_rate
        low = lowcut / nyq
        high = highcut / nyq
        # HOTFIX: how mechanicus of me...
        if high > 1.0:
            high = 0.999
        sos = butter(self.settings.order, [low, high], btype="band", output="sos")
        return sos

    def _apply_filter(self, audio_data, sos):
        return sosfilt(sos, audio_data)

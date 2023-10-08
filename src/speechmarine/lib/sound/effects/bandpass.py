import concurrent
from functools import cache
import numpy as np
from librosa import db_to_amplitude
from scipy.signal import butter, sosfilt

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


# Filter creation can be cached as low/highcut pair can be similar to other one
@cache
def _create_filter(order, lowcut, highcut, sampling_rate):
    nyq = 0.5 * sampling_rate
    low = lowcut / nyq
    high = highcut / nyq
    # HOTFIX: how mechanicus of me...
    if high > 1.0:
        high = 0.999
    return butter(order, [low, high], btype="band", output="sos")


# @profile
def _filter_band(order, audio_data, band, _band0, _band1, sampling_rate):
    sos = _create_filter(order, _band0, _band1, sampling_rate)
    filtered_band = sosfilt(sos, audio_data)
    return filtered_band * db_to_amplitude(band)  # apply gain


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

    # @profile
    def apply(self, audio_data, sampling_rate):
        # TODO: make better bands to reflect DAWs
        min_freq = 31.0  # TODO: what <31 k means?
        max_freq = 25000.0  # TODO: what > 25k Hz means?
        _bands = np.geomspace(min_freq, max_freq, num=self.settings.num_bands + 1)
        filtered_audio = np.zeros_like(audio_data)
        # # Original sequential code:
        # for i in range(self.settings.num_bands):
        #     sos = _create_filter(self.settings.order, _bands[i], _bands[i + 1], sampling_rate)
        #     filtered_band = sosfilt(sos, audio_data)
        #     filtered_audio += filtered_band * db_to_amplitude(
        #         self.settings.bands[i]
        #     )  # apply gain
        # # Pararrel version, scipy.signal.sosfilt is nogil.
        # # ref: https://github.com/scipy/scipy/blob/166e1f2b1ea0a1a2c3d7b030bd829549f8a5844a/scipy/signal/_sosfilt.pyx#L19-L31
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.settings.num_bands) as executor:
            future_to_index = {
                executor.submit(
                    _filter_band, self.settings.order, audio_data, self.settings.bands[index], _bands[index], _bands[index + 1], sampling_rate
                ): index for index in range(self.settings.num_bands)
            }
            for future in concurrent.futures.as_completed(future_to_index):
                filtered_band = None
                try:
                    filtered_band = future.result()
                except Exception as exc:
                    # TODO: replace with a proper error raise
                    print(f"Filter on band #{future_to_index[future]} generated an exception: {exc}")
                filtered_audio += filtered_band

        return filtered_audio * db_to_amplitude(
            self.settings.gain
        )  # apply overall gain at the end

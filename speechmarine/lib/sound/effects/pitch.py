import librosa

from speechmarine.lib.sound.effects.effect import Effect
from speechmarine.lib.sound.effects.settings import Settings


class PitchSettings(Settings):
    def __init__(self, semitones, cents) -> None:
        self._semitones = semitones
        # TODO: assert cents are in range (-100, +100)
        self._cents = cents

    @property
    def semitones(self):
        return self._semitones

    @semitones.setter
    def semitones(self, value):
        self._semitones = value

    @property
    def cents(self):
        return self._cents

    @cents.setter
    def cents(self, value):
        self._cents = value


class Pitch(Effect[PitchSettings]):
    """TODO"""

    def __init__(self, semitones, cents) -> None:
        self._settings = PitchSettings(semitones, cents)

    def apply(self, audio_data, sampling_rate):
        _steps = self.settings.semitones + self.settings.cents * 0.01
        return librosa.effects.pitch_shift(
            audio_data, sr=sampling_rate, n_steps=_steps, res_type="soxr_vhq"
        )

from typing import Any

from speechmarine.lib.sound import Chain
from speechmarine.lib.sound.effects import *  # TODO: import only used ones?


class PresetBase:
    def __init__(self, chain: Chain) -> None:
        """Initialize the preset with Chain class.

        Args:
            chain (Chain): A sequence of Effect instances.
        """
        self.chain = chain

    def __call__(self, audio_data: Any, sampling_rate: float, times: int = 1) -> Any:
        """Process the input audio data by applying all the effects in the chain.

        Args:
            audio_data (Any): The input audio data.
            sampling_rate (float): The sampling rate of the audio data.
            times (int): How many times to repeat the chain.

        Returns:
            Any: The processed audio data after applying all the effects from Chain.
        """
        if times < 1:
            raise ValueError(f"'times' value should be 1 or more! Recieved: {times}")

        for _ in range(times):
            audio_data = self.chain(audio_data=audio_data, sampling_rate=sampling_rate)

        return audio_data


class SpaceMarinePreset(PresetBase):
    # 1 step applying pitch shift
    # 100 cents in semitone --> -1.5 to pitch down 1 semitone and 50 cents
    # 2 step applying echo
    # 3 step - "Fat Snare" - TODO: figure out how it works, especially attack/release and threshold
    # 4 step - equalizer 30 bands
    # 5 step - "Boomy Kick" TODO: as for Fat Snare
    # 6 step - equalizer 20 bands
    # 7 step - equalizer 20 bands
    # 8 step - mastering
    # 8.1 - reverb
    # 8.2 - exciter
    # 9 step - "Desser light" TODO: as for Fat Snare
    def __init__(self) -> None:
        super().__init__(
            Chain(
                Pitch(semitones=-1, cents=-50),
                Echo(delay=0, feedback=0.6, attenuation=1.0),
                Echo(delay=0, feedback=0.6, attenuation=1.0),
                Compressor(
                    threshold=-30.0, ratio=4.0, attack=10, release=100, gain=0.0
                ),
                Bandpass(
                    bands=[
                        4.5,
                        6.0,
                        7.5,
                        7.5,
                        5.0,
                        3.0,
                        1.5,
                        0.5,
                        0.0,
                        -0.5,
                        -1.5,
                        -3.0,
                        -5.0,
                        -3.0,
                        -1.5,
                        0.0,
                        1.5,
                        3.0,
                        3.0,
                        3.0,
                        1.5,
                        0.0,
                        0.0,
                        3.0,
                        6.0,
                        7.5,
                        7.5,
                        6.0,
                        3.0,
                        0.0,
                    ],
                    num_bands=30,
                    order=1,
                    gain=-3.0,
                ),
                Compressor(threshold=-30.0, ratio=5.0, attack=10, release=10, gain=5.0),
                Bandpass(
                    bands=[
                        -3.0,
                        3.0,
                        6.0,
                        4.5,
                        3.0,
                        3.5,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        2.0,
                        3.0,
                        4.0,
                        4.0,
                        4.0,
                        4.0,
                    ],
                    num_bands=20,
                    order=1,
                    gain=-2.0,
                ),
                Bandpass(
                    bands=[
                        0.0,
                        0.0,
                        5.2,
                        6.0,
                        3.2,
                        0.0,
                        -11.6,
                        -5.2,
                        -4.0,
                        -4.0,
                        0.0,
                        3.2,
                        4.8,
                        0.0,
                        0.0,
                        0.0,
                        -3.2,
                        -7.2,
                        -10.8,
                        -14.0,
                    ],
                    num_bands=20,
                    order=1,
                    gain=-5.0,
                ),
                Reverb(dry=0.95, wet=0.15, wide=0.3),
                Exciter(cutoff=13000, order=1, gain=-16.0),
                # 8.3 - TODO: widerer
                # 8.4 - TODO: one-point EQ, instead of 8-bands?
                Bandpass(
                    bands=[0.0, 0.0, 0.0, 0.0, 0.3, 1.2, 0.3, 0.0],
                    num_bands=8,
                    order=3,
                    gain=1.0,
                ),
                Compressor(
                    threshold=-30.0, ratio=1.5, attack=1000, release=1000, gain=0.0
                ),
                Normalizer(),
            )
        )


class DreadnoughtPreset(PresetBase):
    def __init__(self) -> None:
        super().__init__(
            Chain(
                Echo(delay=10, feedback=0.5, attenuation=1.0),
                Echo(delay=10, feedback=0.5, attenuation=1.0),
                Compressor(threshold=-30.0, ratio=5.0, attack=10, release=10, gain=5.0),
                Compressor(threshold=-30.0, ratio=5.0, attack=10, release=10, gain=5.0),
                # TODO: DeEsser
                # TODO
                Bandpass(
                    bands=[
                        0.0,
                        0.0,
                        5.2,
                        6.0,
                        3.2,
                        0.0,
                        -11.6,
                        -5.2,
                        -4.0,
                        -4.0,
                        0.0,
                        3.2,
                        4.8,
                        0.0,
                        0.0,
                        0.0,
                        -3.2,
                        -7.2,
                        -10.8,
                        -14.0,
                    ],
                    num_bands=20,
                    order=1,
                    gain=-5.0,
                ),
                # TODO
                Bandpass(
                    bands=[
                        0.0,
                        0.0,
                        5.2,
                        6.0,
                        3.2,
                        0.0,
                        -11.6,
                        -5.2,
                        -4.0,
                        -4.0,
                        0.0,
                        3.2,
                        4.8,
                        0.0,
                        0.0,
                        0.0,
                        -3.2,
                        -7.2,
                        -10.8,
                        -14.0,
                    ],
                    num_bands=20,
                    order=1,
                    gain=-5.0,
                ),
                Compressor(threshold=-30.0, ratio=5.0, attack=10, release=10, gain=5.0),
                # TODO
                Bandpass(
                    bands=[
                        4.5,
                        6.0,
                        7.5,
                        7.5,
                        5.0,
                        3.0,
                        1.5,
                        0.5,
                        0.0,
                        -0.5,
                        -1.5,
                        -3.0,
                        -5.0,
                        -3.0,
                        -1.5,
                        0.0,
                        1.5,
                        3.0,
                        3.0,
                        3.0,
                        1.5,
                        0.0,
                        0.0,
                        3.0,
                        6.0,
                        7.5,
                        7.5,
                        6.0,
                        3.0,
                        0.0,
                    ],
                    num_bands=30,
                    order=1,
                    gain=-3.0,
                ),
                Pitch(semitones=-5, cents=-100),
                Reverb(dry=0.85, wet=0.5, wide=0.65),
                Normalizer(),
            )
        )

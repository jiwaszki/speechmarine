from typing import Any, Type

from speechmarine.lib.sound.effects.effect import Effect


class Chain:
    def __init__(self, *effects: Type[Effect]) -> None:
        """Initialize the Chain class with a sequence of Effect instances.

        Args:
            *effects (Type[Effect]): A sequence of Effect instances.
        """
        self.effects = effects

    def __call__(self, audio_data: Any, sampling_rate: float) -> Any:
        """Process the input audio data by applying all the effects in the chain.

        Args:
            audio_data (Any): The input audio data.
            sampling_rate (float): The sampling rate of the audio data.

        Returns:
            Any: The processed audio data after applying all the effects.
        """
        for effect in self.effects:
            audio_data = effect.apply(audio_data, sampling_rate)

        return audio_data

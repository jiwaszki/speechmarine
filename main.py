import time
import logging
import coloredlogs
import librosa
import sounddevice as sd
import soundfile as sf
from speechmarine.lib.presets import SpaceMarinePreset, DreadnoughtPreset
import argparse

# Constants
TARGET_SAMPLING_RATE = 44100
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"


def load_audio(file_path):
    """
    Load audio from a file and return the audio data and sampling rate.
    """
    audio_data, sampling_rate = librosa.load(file_path, sr=None)
    return audio_data, sampling_rate


def check_and_resample(audio_data, sampling_rate):
    """
    Check if audio needs resampling and perform it if necessary.
    """
    if sampling_rate != TARGET_SAMPLING_RATE:
        logging.warning("Audio file is going to be up- or down-sampled during runtime!")
        audio_data = librosa.resample(
            audio_data, orig_sr=sampling_rate, target_sr=TARGET_SAMPLING_RATE
        )
        sampling_rate = TARGET_SAMPLING_RATE
    return audio_data, sampling_rate


def apply_preset(audio_data, sampling_rate, preset_name, times):
    """
    Apply a preset to the audio data.
    """
    preset = get_preset_by_name(preset_name)
    return preset(audio_data=audio_data, sampling_rate=sampling_rate, times=times)


def get_preset_by_name(name):
    """
    Get a preset instance by name. Raises a ValueError if the name is invalid.
    """
    preset_mapping = {
        "spacemarine": SpaceMarinePreset(),
        "dreadnought": DreadnoughtPreset(),
    }

    name = name.lower()
    preset = preset_mapping.get(name)
    if preset is None:
        raise ValueError(f"Invalid preset name: {name}")

    return preset


def play_audio(audio_data, sampling_rate):
    """
    Play audio using sounddevice.
    """
    sd.play(audio_data, samplerate=sampling_rate)
    sd.wait()


def save_audio(file_path, audio_data, sampling_rate):
    """
    Save audio data to a file using soundfile.
    """
    sf.write(file_path, audio_data, sampling_rate, subtype="PCM_24")


def main():
    parser = argparse.ArgumentParser(description="Audio Processing Script")
    parser.add_argument(
        "--input", type=str, required=True, help="Input audio file path"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="speechmarine_generation.wav",
        help="Output audio file path (default: speechmarine_generation.wav)",
    )
    parser.add_argument(
        "--preset",
        choices=["spacemarine", "dreadnought"],
        required=True,
        help="Preset to apply",
    )
    parser.add_argument(
        "--times",
        type=int,
        default=1,
        help="Number of times to apply the preset (default: 1)",
    )
    args = parser.parse_args()

    coloredlogs.install(level="INFO", fmt=LOG_FORMAT)

    # Load audio
    audio_data, sampling_rate = load_audio(args.input)

    # Check and possibly resample audio
    audio_data, sampling_rate = check_and_resample(audio_data, sampling_rate)

    start_time = time.time()

    # Apply the selected preset
    audio_data = apply_preset(audio_data, sampling_rate, args.preset, args.times)

    end_time = time.time()

    logging.info(f"Processing time: {end_time - start_time}")

    # Play and save audio
    play_audio(audio_data, sampling_rate)
    save_audio(args.output, audio_data, sampling_rate)


if __name__ == "__main__":
    main()


# SpeechMarine Audio Library and Application

SpeechMarine library defining presets and scripts. It allows you to apply presets to an input audio file and save the processed audio to an output file.

Mostly a fun project to learn few new things (building systems and dependency managers), write some audio algorithms and possibly add some AI solutions to it... or even GUI.

Big thanks to [DreadAnon](https://www.youtube.com/@DreadAnon/about) who described [the process of recreating those epic effects](https://www.youtube.com/watch?v=VNsVkIWhvTk). This project also use a sample from DreadAnon's video (if this project ever reaches you, please do not send Ordo Hereticus after me... just let me know if I need to remove it!).

## Installation

Make sure you have Python 3.9 or later installed. You can install the required dependencies using [PDM](https://pdm.fming.dev/). When inside the project directory, simply run the following commands:

```bash
pip install --upgrade pip
pip install pdm
pdm install --plugins
pdm custom-install --python env --no-lock
# Run demo to verify installation
pdm run demo
```

The strongly recommended approach is to use a custom installation plugin (located in the `pdm-custom-plugins` directory). This plugin allows you to specify Python versions using the `--python` flag. Since `PDM`` tries to resolve all dependencies across a wide range of versions, it can be beneficial to use the most recent ones for your specific Python version. For example, you can use the most recent version of numpy to benefit from the latest optimizations.

The plugin is built on top of the `pdm install` command, so all other flags work exactly the same way.

First, install project's plugins:
```bash
pdm install --plugins
```

You can use the plugin in a variety of ways:

- Install using your current environment's version of Python:

    ```bash
    pdm custom-install --python env --no-self --no-lock
    # or you replace both '--no-self' and '--no-lock' with '--requirements'
    pdm custom-install --requirements --python env
    ```

- Specify the Python version yourself:

    ```bash
    pdm custom-install --python ">3.9" --no-self --no-lock
    # or
    pdm custom-install --python ">=3.9, <3.11" --no-self --no-lock
    ```

- Use the `python.version` config variable to remember the setting:

    ```bash
    pdm config python.version "==$(python -V | cut -d' ' -f2)"
    pdm custom-install --no-self --no-lock
    ```

## Usage

```bash
python main.py --input INPUT_AUDIO --output OUTPUT_AUDIO --preset PRESET_NAME [--times TIMES]
```

- `INPUT_AUDIO`: Path to the input audio file.
- `OUTPUT_AUDIO`: Path to the output audio file (default: "speechmarine_generation.wav").
- `PRESET_NAME`: Name of the preset to apply ("spacemarine" or "dreadnought").
- `TIMES` (optional): Number of times to apply the preset (default: 1).

Example commands:

```bash
# Dreadnought voice effect with default save
python main.py --input ./sample.wav --preset dreadnought --times 1
# Space Marine voice effect with custom save
python main.py --input ./sample.wav --output ./output_audio.wav --preset spacemarine --times 1
```

## Configuration

The library relies on the project configuration from the `pyproject.toml` file.

## License

TBA

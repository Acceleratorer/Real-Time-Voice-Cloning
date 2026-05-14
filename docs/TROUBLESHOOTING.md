# Troubleshooting

Run the setup doctor first:

```bash
uv run --extra cpu voice-clone-doctor
```

Use strict mode in CI or scripts:

```bash
uv run --extra cpu voice-clone-doctor --strict
```

## `ffmpeg` is not found

Install FFmpeg and make sure its `bin` directory is on `PATH`.

Verify with:

```bash
ffmpeg -version
```

## Python version mismatch

This project expects Python 3.9.

Run:

```bash
uv python install 3.9
uv python pin 3.9
uv sync --extra cpu --dev
```

## CUDA is not detected

First verify PyTorch sees CUDA:

```bash
uv run --extra cuda python -c "import torch; print(torch.cuda.is_available())"
```

If this prints `False`, check your NVIDIA driver, CUDA compatibility, and whether the CUDA extra was used during `uv sync`.

To force CPU mode:

```bash
uv run --extra cpu clone_voice.py --cpu --reference samples/p240_00000.mp3 --text "Test sentence." --output outputs/test.wav
```

## Model download fails

Models are downloaded from:

```text
https://huggingface.co/CorentinJ/SV2TTS
```

If automatic download fails, download these files manually:

```text
encoder.pt
synthesizer.pt
vocoder.pt
```

Place them under:

```text
saved_models/default/
```

Then rerun with:

```bash
uv run --extra cpu clone_voice.py --no_auto_download --reference samples/p240_00000.mp3 --text "Test sentence." --output outputs/test.wav
```

## Audio output sounds poor

This is a reproduction of an older SV2TTS stack. It is useful for understanding the pipeline, dependency management, and model orchestration, but it will not match current commercial or state-of-the-art voice cloning systems.

Quality usually improves with:

- A clean reference recording
- One speaker only
- Low background noise
- Five to ten seconds of speech
- A short text prompt for first tests

## `webrtcvad` warnings

`webrtcvad` enables silence trimming. It is optional because it may require Microsoft C++ Build Tools on Windows.

Install it only if you need VAD-based silence trimming:

```bash
uv sync --extra cpu --extra vad --dev
```

If it is not installed, preprocessing still works, but long silence removal is skipped.

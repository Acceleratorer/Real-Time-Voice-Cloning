# Windows Setup

This guide targets Windows users who want to run the toolbox or the non-interactive `clone_voice.py` demo.

## Requirements

- Windows 10 or newer
- Python 3.9 managed by `uv`
- FFmpeg available on `PATH`
- Optional: NVIDIA GPU with CUDA-compatible PyTorch wheels

## 1. Install FFmpeg

Install FFmpeg from one of the builds linked on the official download page:

```text
https://ffmpeg.org/download.html#get-packages
```

After installation, open a new terminal and verify:

```powershell
ffmpeg -version
```

If Windows cannot find `ffmpeg`, add the FFmpeg `bin` directory to your `PATH`, then reopen the terminal.

## 2. Install uv

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```powershell
uv --version
```

## 3. Sync Dependencies

CPU-only environment:

```powershell
uv sync --extra cpu --dev
```

CUDA environment:

```powershell
uv sync --extra cuda --dev
```

The project pins Python to `>=3.9,<3.10` because the original dependency stack is old and some wheels are version-sensitive.

`webrtcvad` is optional on Windows because it may require Microsoft C++ Build Tools. Install it with `--extra vad` only if you need VAD-based silence trimming.

## 4. Run Tests

```powershell
uv run pytest -q
```

## 5. Check Your Setup

```powershell
uv run --extra cpu voice-clone-doctor
```

## 6. Run a Demo

CPU:

```powershell
uv run --extra cpu clone-voice --reference samples/p240_00000.mp3 --text "Welcome to my real-time voice cloning experiment." --output outputs/demo_output.wav
```

CUDA:

```powershell
uv run --extra cuda clone-voice --reference samples/p240_00000.mp3 --text "Welcome to my real-time voice cloning experiment." --output outputs/demo_output.wav
```

The first run downloads pretrained models into `saved_models/default/`.

## Audio Devices

The `clone_voice.py` workflow writes a WAV file and does not require a microphone or playback device. Use `demo_toolbox.py` only after the command-line path works.

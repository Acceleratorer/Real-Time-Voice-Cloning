# Benchmarking

Use `clone_voice.py` for local benchmark runs. It prints stage timings for model loading, speaker encoding, spectrogram synthesis, and waveform generation.

## Command

CPU:

```bash
uv run --extra cpu clone_voice.py --reference samples/p240_00000.mp3 --text "Welcome to my real-time voice cloning experiment." --output outputs/benchmark_cpu.wav
```

CUDA:

```bash
uv run --extra cuda clone_voice.py --reference samples/p240_00000.mp3 --text "Welcome to my real-time voice cloning experiment." --output outputs/benchmark_cuda.wav
```

## Results Template

Record your actual machine details before publishing benchmark numbers.

| Field | Value |
| --- | --- |
| CPU | TBD |
| GPU | TBD |
| RAM | TBD |
| OS | TBD |
| Python | 3.9 |
| PyTorch | TBD |

| Mode | Reference Audio | Text Length | Load Models | Encode | Synthesize | Vocode | Output |
|---|---:|---:|---:|---:|---:|---:|---|
| CPU | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| CUDA | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Notes

- First-run model download time should not be included in inference benchmarks.
- Run each mode at least twice and report whether the number is cold-start or warm-start.
- Keep text and reference audio the same across CPU and CUDA comparisons.
- Generated files under `outputs/` are ignored by git.

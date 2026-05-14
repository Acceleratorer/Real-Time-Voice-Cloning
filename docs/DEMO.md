# Demo Artifact

The generated audio demo is published as a GitHub Release asset instead of being committed to the repository:

[demo-audio-v1](https://github.com/Acceleratorer/Real-Time-Voice-Cloning/releases/tag/demo-audio-v1)

## Published Input

| Field | Value |
| --- | --- |
| Reference audio | `assets/benchmark_reference.wav` |
| Text prompt | `Welcome to my real-time voice cloning experiment.` |
| Output artifact | `demo_output_cuda.wav` |
| Hardware | NVIDIA GeForce RTX 3050 Ti Laptop GPU, 4GB |
| PyTorch | 1.10.2+cu113 |

## Reproduce Locally

```bash
uv run --extra cuda clone-voice \
  --reference assets/benchmark_reference.wav \
  --text "Welcome to my real-time voice cloning experiment." \
  --output outputs/demo_output_cuda.wav \
  --no_trim_output
```

Use CPU only:

```bash
uv run --extra cuda clone-voice \
  --cpu \
  --reference assets/benchmark_reference.wav \
  --text "Welcome to my real-time voice cloning experiment." \
  --output outputs/demo_output_cpu.wav \
  --no_trim_output
```

The repository keeps the small reference WAV and spectrogram image in git, while generated WAV outputs stay in `outputs/` and are ignored to avoid unnecessary repository size growth.

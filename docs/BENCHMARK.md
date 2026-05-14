# Benchmarking

Use `clone_voice.py` for local benchmark runs. It prints stage timings for model loading, speaker encoding, spectrogram synthesis, and waveform generation.

## Command

CPU:

```bash
uv run --extra cuda clone-voice --cpu --reference assets/benchmark_reference.wav --text "Welcome to my real-time voice cloning experiment." --output outputs/benchmark_cpu.wav --no_trim_output
```

CUDA:

```bash
uv run --extra cuda clone-voice --reference assets/benchmark_reference.wav --text "Welcome to my real-time voice cloning experiment." --output outputs/benchmark_cuda.wav --no_trim_output
```

## Local Results

These numbers are a single warm run after pretrained models were already downloaded. They are useful for reproduction notes, not as a formal model benchmark.

| Field | Value |
| --- | --- |
| CPU | Ryzen 7 4800H |
| GPU | NVIDIA GeForce RTX 3050 Ti Laptop GPU, 4GB |
| RAM | 16GB |
| OS | Windows 10 10.0.26200 |
| Python | 3.9.25 |
| PyTorch | 1.10.2+cu113 |
| NVIDIA driver | 496.49 |
| Reference audio | Generated 5s WAV, `assets/benchmark_reference.wav` |
| Text prompt | `Welcome to my real-time voice cloning experiment.` |

| Mode | Reference Audio | Text Length | Load Models | Encode | Synthesize | Vocode | Output |
|---|---:|---:|---:|---:|---:|---:|---|
| CPU | 5s | 7 words | 0.13s | 0.13s | 1.43s | 18.86s | `outputs/demo_output_cpu.wav` |
| CUDA | 5s | 7 words | 4.60s | 2.25s | 4.39s | 17.19s | `outputs/demo_output_cuda.wav` |

The CUDA output from this benchmark is published as the [demo-audio-v1 release](https://github.com/Acceleratorer/Real-Time-Voice-Cloning/releases/tag/demo-audio-v1).

## Notes

- First-run model download time should not be included in inference benchmarks.
- Run each mode at least twice and report whether the number is cold-start or warm-start.
- Keep text and reference audio the same across CPU and CUDA comparisons.
- Generated files under `outputs/` are ignored by git.
- FFmpeg was not on `PATH` during this run, so the benchmark used a generated WAV reference instead of the bundled MP3 samples.

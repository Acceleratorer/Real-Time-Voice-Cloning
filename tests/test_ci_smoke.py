import os
import sys

# Ensure the repository root is on sys.path for imports like `import encoder`
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def test_third_party_imports():
    import librosa  # noqa: F401
    import numpy  # noqa: F401
    import soundfile  # noqa: F401
    import torch  # noqa: F401


def test_project_imports():
    import encoder  # noqa: F401
    import synthesizer  # noqa: F401
    import vocoder  # noqa: F401


def test_encoder_preprocess_handles_silence():
    import numpy as np
    from encoder import inference as encoder

    wav = np.zeros(encoder.sampling_rate, dtype=np.float32)
    processed = encoder.preprocess_wav(wav, encoder.sampling_rate, trim_silence=False)

    assert processed.ndim == 1
    assert processed.dtype in (np.float32, np.float64)
    assert np.all(np.isfinite(processed))
    assert np.allclose(processed, 0)


def test_clone_voice_parser_defaults():
    from clone_voice import DEFAULT_OUTPUT, build_parser, resolve_model_paths

    args = build_parser().parse_args([
        "--reference",
        "samples/p240_00000.mp3",
        "--text",
        "Welcome to my real-time voice cloning experiment.",
    ])
    enc_model, syn_model, voc_model = resolve_model_paths(args)

    assert args.output == DEFAULT_OUTPUT
    assert enc_model.name == "encoder.pt"
    assert syn_model.name == "synthesizer.pt"
    assert voc_model.name == "vocoder.pt"


def test_doctor_python_version_check_accepts_project_python():
    from types import SimpleNamespace

    from doctor import check_python_version

    ok, label = check_python_version(SimpleNamespace(major=3, minor=9, micro=18))

    assert ok
    assert "Python 3.9.18" in label


def test_doctor_model_file_checks_missing_dir(tmp_path):
    from doctor import DEFAULT_MODEL_SIZES, check_model_files

    results = check_model_files(tmp_path / "missing")

    assert len(results) == len(DEFAULT_MODEL_SIZES)
    assert all(not ok for ok, _ in results)

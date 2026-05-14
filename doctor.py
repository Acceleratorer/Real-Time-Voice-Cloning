import argparse
import importlib.util
import shutil
import sys
from pathlib import Path


REQUIRED_PYTHON = (3, 9)
MAX_PYTHON = (3, 10)
DEFAULT_MODELS_DIR = Path("saved_models") / "default"
DEFAULT_MODEL_SIZES = {
    "encoder.pt": 17090379,
    "synthesizer.pt": 370554559,
    "vocoder.pt": 53845290,
}
CORE_PACKAGES = [
    "librosa",
    "numpy",
    "scipy",
    "soundfile",
    "torch",
    "webrtcvad",
]


def check_python_version(version_info=None):
    version_info = version_info or sys.version_info
    current = (version_info.major, version_info.minor)
    ok = REQUIRED_PYTHON <= current < MAX_PYTHON
    detail = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    expected = f">={REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]},<{MAX_PYTHON[0]}.{MAX_PYTHON[1]}"
    return ok, f"Python {detail} ({expected} required)"


def check_ffmpeg():
    path = shutil.which("ffmpeg")
    return path is not None, path or "ffmpeg not found on PATH"


def check_package(module_name):
    installed = importlib.util.find_spec(module_name) is not None
    return installed, module_name


def check_model_files(models_dir=DEFAULT_MODELS_DIR):
    results = []
    for filename, expected_size in DEFAULT_MODEL_SIZES.items():
        path = models_dir / filename
        if not path.exists():
            results.append((False, f"{path} missing"))
            continue
        size = path.stat().st_size
        ok = size == expected_size
        status = f"{path} {size} bytes"
        if not ok:
            status += f" (expected {expected_size})"
        results.append((ok, status))
    return results


def format_result(ok, label):
    mark = "OK" if ok else "!!"
    return f"[{mark}] {label}"


def run_checks(models_dir=DEFAULT_MODELS_DIR):
    checks = []
    checks.append(check_python_version())
    checks.append(check_ffmpeg())
    checks.extend(check_package(package) for package in CORE_PACKAGES)
    checks.extend(check_model_files(models_dir))
    return checks


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check local setup for the voice cloning pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--models_dir",
        type=Path,
        default=DEFAULT_MODELS_DIR,
        help="Directory containing encoder.pt, synthesizer.pt, and vocoder.pt.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any check fails.",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    checks = run_checks(args.models_dir)

    print("Real-Time Voice Cloning setup check")
    for ok, label in checks:
        print(format_result(ok, label))

    failed = [label for ok, label in checks if not ok]
    if failed:
        print("\nSome checks failed. See docs/TROUBLESHOOTING.md for fixes.")
        return 1 if args.strict else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

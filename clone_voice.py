import argparse
import os
import time
from pathlib import Path


DEFAULT_MODELS_DIR = Path("saved_models")
DEFAULT_OUTPUT = Path("outputs") / "result.wav"


def build_parser():
    parser = argparse.ArgumentParser(
        description="Clone a reference voice into a generated WAV file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-r",
        "--reference",
        type=Path,
        required=True,
        help="Path to a reference voice audio file.",
    )
    parser.add_argument(
        "-t",
        "--text",
        required=True,
        help="Text prompt to synthesize with the reference voice.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path where the generated WAV file will be written.",
    )
    parser.add_argument(
        "--models_dir",
        type=Path,
        default=DEFAULT_MODELS_DIR,
        help="Directory containing or receiving the default pretrained models.",
    )
    parser.add_argument(
        "-e",
        "--enc_model_fpath",
        type=Path,
        default=None,
        help="Path to a saved speaker encoder model.",
    )
    parser.add_argument(
        "-s",
        "--syn_model_fpath",
        type=Path,
        default=None,
        help="Path to a saved synthesizer model.",
    )
    parser.add_argument(
        "-v",
        "--voc_model_fpath",
        type=Path,
        default=None,
        help="Path to a saved vocoder model.",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Force inference to run on CPU even when CUDA is available.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for reproducible synthesis experiments.",
    )
    parser.add_argument(
        "--no_auto_download",
        action="store_true",
        help="Do not download default models before inference.",
    )
    parser.add_argument(
        "--vocoder_target",
        type=int,
        default=8000,
        help="WaveRNN target segment length. Larger values are usually higher quality.",
    )
    parser.add_argument(
        "--vocoder_overlap",
        type=int,
        default=800,
        help="WaveRNN segment overlap.",
    )
    parser.add_argument(
        "--no_trim_output",
        action="store_true",
        help="Skip the final silence-trimming pass on generated audio.",
    )
    return parser


def resolve_model_paths(args):
    default_dir = args.models_dir / "default"
    return (
        args.enc_model_fpath or default_dir / "encoder.pt",
        args.syn_model_fpath or default_dir / "synthesizer.pt",
        args.voc_model_fpath or default_dir / "vocoder.pt",
    )


def _elapsed_since(start_time):
    return time.perf_counter() - start_time


def clone_voice(args):
    if args.cpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    import numpy as np
    import soundfile as sf
    import torch

    from encoder import inference as encoder
    from synthesizer.inference import Synthesizer
    from utils.default_models import ensure_default_models
    from vocoder import inference as vocoder

    if args.seed is not None:
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)

    enc_model_fpath, syn_model_fpath, voc_model_fpath = resolve_model_paths(args)
    timings = {}

    stage_start = time.perf_counter()
    if not args.no_auto_download:
        ensure_default_models(args.models_dir)
    encoder.load_model(enc_model_fpath)
    synthesizer = Synthesizer(syn_model_fpath)
    vocoder.load_model(voc_model_fpath)
    timings["load_models"] = _elapsed_since(stage_start)

    stage_start = time.perf_counter()
    preprocessed_wav = encoder.preprocess_wav(args.reference)
    if preprocessed_wav.size == 0:
        raise ValueError(
            "Reference audio has no voiced samples after preprocessing. "
            "Try a cleaner clip with a few seconds of speech."
        )
    embed = encoder.embed_utterance(preprocessed_wav)
    timings["encode_reference"] = _elapsed_since(stage_start)

    stage_start = time.perf_counter()
    spec = synthesizer.synthesize_spectrograms([args.text], [embed])[0]
    timings["synthesize_mel"] = _elapsed_since(stage_start)

    stage_start = time.perf_counter()
    generated_wav = vocoder.infer_waveform(
        spec,
        target=args.vocoder_target,
        overlap=args.vocoder_overlap,
    )
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    if not args.no_trim_output:
        generated_wav = encoder.preprocess_wav(generated_wav, synthesizer.sample_rate)
    timings["vocode_waveform"] = _elapsed_since(stage_start)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(args.output), generated_wav.astype(np.float32), synthesizer.sample_rate)

    print(f"\nWrote generated audio to {args.output}")
    print("Stage timings:")
    for name, seconds in timings.items():
        print(f"  {name}: {seconds:.2f}s")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.reference.is_file():
        parser.error(f"Reference audio does not exist: {args.reference}")
    if not args.text.strip():
        parser.error("Text prompt cannot be empty.")
    if args.vocoder_target <= 0:
        parser.error("--vocoder_target must be positive.")
    if args.vocoder_overlap < 0:
        parser.error("--vocoder_overlap cannot be negative.")
    if args.vocoder_overlap >= args.vocoder_target:
        parser.error("--vocoder_overlap must be smaller than --vocoder_target.")

    clone_voice(args)


if __name__ == "__main__":
    main()

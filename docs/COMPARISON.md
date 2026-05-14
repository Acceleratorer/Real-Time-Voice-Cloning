# Comparison With Upstream

This fork is intentionally positioned as a modernization and reproducibility project, not as a from-scratch replacement for the original SV2TTS implementation.

| Area | CorentinJ upstream | Acceleratorer fork |
| --- | --- | --- |
| Core SV2TTS pipeline | Speaker encoder, synthesizer, vocoder | Preserved and documented |
| Dependency workflow | Modern `uv` support from upstream | Kept, documented, and exposed in quick-start flow |
| GitHub Actions | Import and smoke tests | Kept, with extra parser and preprocessing coverage |
| Pretrained models | Automatic Hugging Face download | Kept, with model file checks in `voice-clone-doctor` |
| CLI workflow | Interactive `demo_cli.py` | Adds non-interactive `clone_voice.py` and `clone-voice` entry point |
| Setup diagnostics | Manual troubleshooting | Adds `doctor.py` and `voice-clone-doctor` entry point |
| Portfolio positioning | Original thesis implementation | Clear modernized-fork positioning and contribution summary |
| Responsible use | Not prominent in original README | Explicit safety and consent guidance |
| Windows guidance | Basic support note | Dedicated setup and troubleshooting docs |

## Why This Fork Is Different

The original repository is valuable because it implements the classic SV2TTS architecture. This fork is valuable because it makes the project easier to reproduce, inspect, and present:

- A visitor can understand the architecture from the README and docs.
- A user can run a non-interactive command instead of stepping through prompts.
- A maintainer can run CI and setup diagnostics before trying full model inference.
- A recruiter can see concrete modernization work rather than a silent fork.

## Current Upgrade Focus

The strongest upgrades are operational rather than model-level:

- Reproducible install path
- CI and lightweight functional tests
- Setup diagnostics
- Documentation for Windows and benchmarks
- Clear ethical-use language

Future work should focus on demo artifacts, benchmark results from real hardware, and optional quality improvements that do not hide the age of the underlying model stack.

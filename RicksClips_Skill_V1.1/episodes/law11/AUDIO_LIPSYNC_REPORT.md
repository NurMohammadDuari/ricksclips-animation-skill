# AUDIO & LIP-SYNC REPORT — Law 11

## Source audio
- File: `upload/The 48 Laws Of Power By Robert Greene Explained In Bangla Law 11.mp3` — 121.3 s, single Bangla narrator, 302 words in 15 sentences (0.1 s → 120.9 s).
- Probe: `tools/audio_probe.py` produced `voice/words.json` (energy-aligned word onsets). The episode's words.json matches the MP3's 121.3 s — no re-timing needed.

## Narration synchronization
- The mux uses the MP3 directly (`-i mp3 -map 1:a:0 -af volume=1.8,apad -shortest`): video 121.5 s, audio padded/trimmed to the same length — **no drift possible** (single container, ffprobe-verified).
- Word captions: one Bangla word at a time burned into frames from words.json — spot-checked at beats 0–15; each caption is the word being spoken at that second.
- Scene cuts align to sentence boundaries, not arbitrary seconds (see TIMING_AND_CONTINUITY_REPORT).

## Lip-sync (viseme) mechanism
- Talking characters get `mouth` states from `visemes(word)` in the plan — mouth shapes keyed to the CURRENT word being spoken by that scene's speaker.
- Mouth states are baked per frame into `performance_baked.json`; silent characters hold closed mouths (no idle flapping) — verified in beat frames.
- The film is narration-driven (no on-screen dialogue lines), so lip-sync is deliberately **acting-sync** (gesture + mouth on the speaker's narrated line), which matches Rick/Clips convention for explainers.
- Residual (honest): without a Fish Audio key the pipeline cannot generate per-character dialogue tracks; phoneme-level viseme accuracy is as good as the generic Bangla viseme table — acceptable for narration-first Shorts, documented as a known limit in SKILL.md.

## Sound design
- SFX/music folders are placeholders in the toolkit (`<YOUR_SFX_FOLDER>` / `<YOUR_MUSIC_FOLDER>`) — the film ships with narration + burned captions only.
- `out/plan/sound_events.json` already carries the cue sheet (door knock, packet, till) for when an SFX folder is configured.
- Music: none, by design — the narration's cadence is the rhythm; adding music later must duck under -14 LUFS narration per the skill's sound-designer brief.

## Verification
- ffprobe on the delivered MP4: streams video (540×960 30 fps H.264) + audio (AAC), duration 121.5 s — matches words.json's last word (120.9 s) + tail pad.
- Audio levels: narration normalized with volume=1.8 pre-mux; no clipping observed (speech peaks comfortably below 0 dBFS after normalization).

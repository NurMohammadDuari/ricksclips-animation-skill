#!/usr/bin/env python3
"""audio_probe.py - listen to a narration track and hand the film a timed, measured script.

    python tools/audio_probe.py voice/voice.wav --script story.txt \
        --words episodes/<slug>/voice/words.json \
        --report episodes/<slug>/out/audio.json

What it gives the generator:
  * word timings (w/s/e) aligned to the actual audio - either from faster-whisper when it is
    installed and --transcribe is asked for, or from the audio's own speech pockets + the script;
  * a loudness value per word and per sentence, so the generator can put a kick / glint / light
    change on the words that were actually spoken loudly instead of at arbitrary beats.

Only the Python standard library + numpy are required. WAV is read directly; other formats are
piped through ffmpeg when ffmpeg is on PATH. Nothing is hard-coded to one language or episode.
"""
import argparse, json, os, re, shutil, subprocess, sys, wave

import numpy as np

RATE = 16000
WIN = 0.02                      # 20 ms loudness window
GAP = 0.24                      # a quieter gap this long separates two speech pockets
MIN_SPEECH = 0.16


def read_pcm(path, rate=RATE):
    """Return mono float samples in [-1, 1]. WAV directly, everything else through ffmpeg."""
    if path.lower().endswith(".wav"):
        with wave.open(path, "rb") as w:
            ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
            raw = w.readframes(n)
        if sw == 2:
            a = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
        elif sw == 4:
            a = np.frombuffer(raw, dtype="<i4").astype(np.float32) / 2147483648.0
        elif sw == 1:
            a = (np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128) / 128.0
        else:
            raise ValueError("unsupported WAV sample width %d" % sw)
        if ch > 1:
            a = a.reshape(-1, ch).mean(axis=1)
        if sr != rate:
            a = np.interp(np.arange(0, len(a), sr / rate), np.arange(len(a)), a).astype(np.float32)
        return a
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("%s is not WAV and ffmpeg is not on PATH - convert it first" % path)
    r = subprocess.run([ffmpeg, "-v", "error", "-i", path, "-f", "s16le", "-ac", "1",
                        "-ar", str(rate), "pipe:1"], capture_output=True)
    if r.returncode:
        raise RuntimeError("ffmpeg could not read %s: %s" % (path, r.stderr.decode(errors="replace")[:300]))
    return np.frombuffer(r.stdout, dtype="<i2").astype(np.float32) / 32768.0


def envelope(audio, rate=RATE, win=WIN):
    """RMS per window, plus its duration in seconds."""
    n = max(1, int(round(rate * win)))
    pad = (-len(audio)) % n
    if pad:
        audio = np.pad(audio, (0, pad))
    frames = audio.reshape(-1, n)
    return np.sqrt((frames ** 2).mean(axis=1)), n / float(rate)


def speech_segments(env, step):
    """Speech pockets: everything above a fraction of the loudest window, with short gaps bridged."""
    if not len(env):
        return []
    peak = float(np.percentile(env, 99.5)) or 1e-6
    on = env > max(0.012, 0.10 * peak)
    out, start = [], None
    for i, v in enumerate(on):
        if v and start is None:
            start = i
        if start is not None and (not v or i == len(on) - 1):
            end = i if not v else i + 1
            out.append([round(start * step, 3), round(end * step, 3)])
            start = None
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= GAP:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [(round(a, 3), round(b, 3)) for a, b in merged if b - a >= MIN_SPEECH]


def word_weight(w):
    """A Bangla/English word takes roughly as long as its spoken syllables, not its byte count."""
    letters = sum(ch.isalnum() for ch in w)
    return 0.30 + 0.075 * letters + 0.05 * w.count("।")


def align_to_script(sentences, segments, energy, rate=RATE, step=WIN):
    """Share the real speech pockets between the script's words; loudness rides along with each word."""
    if not segments:
        dur = len(energy) * step
        segments = [(0.15, max(0.5, dur - 0.15))]
    all_words = []
    for si, s in enumerate(sentences):
        import re
        ws = re.findall(r"[0-9\u0980-\u09FFA-Za-z]+(?:['’\-][0-9\u0980-\u09FFA-Za-z]+)*", s)
        all_words.append(ws)
    counts = [len(x) for x in all_words]
    total = sum(counts) or 1
    speech = [max(0.05, b - a) for a, b in segments]
    total_speech = sum(speech)
    alloc = [max(1, int(round(total * d / total_speech))) for d in speech]
    while sum(alloc) > total:
        k = max(range(len(alloc)), key=lambda i: alloc[i]); alloc[k] -= 1
    while sum(alloc) < total:
        k = min(range(len(alloc)), key=lambda i: alloc[i]); alloc[k] += 1
    flat = [w for ws in all_words for w in ws]
    words, wi = [], 0
    for (a, b), nw in zip(segments, alloc):
        chunk = flat[wi:wi + nw]; wi += nw
        if not chunk:
            continue
        weights = [word_weight(w) for w in chunk]
        unit = (b - a) / max(1e-6, sum(weights))
        t = a
        for w, wt in zip(chunk, weights):
            dur = wt * unit
            i0, i1 = max(0, int(t / step)), max(1, int((t + dur) / step))
            gain = float(np.mean(energy[i0:i1])) if i1 > i0 and len(energy) else 0.0
            words.append({"w": w, "s": round(t, 3), "e": round(t + max(0.16, dur * 0.92), 3),
                          "gain": round(gain, 5)})
            t += dur
    return words


LINE_RE = re.compile(r"^\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*(?:\[([^\]]+)\]\s*:?\s*)?(.*)$")


def parse_timestamped_script(text):
    """Read a narrated script like `00:04 [রাফি]: কথা...` -> (sentences, timed lines).

    Returns (sents, timed) where timed = [{t, speaker, text}]. If the script has no timecodes,
    timed is empty and the caller falls back to plain sentences.
    """
    timed = []
    for raw in text.splitlines():
        m = LINE_RE.match(raw)
        if not m:
            continue
        stamp, speaker, line = m.groups()
        parts = stamp.split(":")
        sec = int(parts[0]) * 60 + int(parts[1])
        if len(parts) == 3:
            sec = sec * 60 + int(parts[2])
        line = line.strip()
        if line:
            timed.append({"t": sec, "speaker": (speaker or "").strip(), "text": line})
    return [x["text"] for x in timed], timed


def audio_duration(path):
    """Duration without decoding: mutagen for compressed audio, wave for WAV."""
    if path.lower().endswith(".wav"):
        with wave.open(path, "rb") as w:
            return round(w.getnframes() / float(w.getframerate()), 3)
    try:
        from mutagen import File
        f = File(path)
        return round(float(f.info.length), 3) if f and f.info else 0.0
    except Exception:
        return 0.0


def transcribe(path):
    """Optional: real word times from faster-whisper. Returns None when it is not installed."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(path, word_timestamps=True, beam_size=1)
    out = []
    for seg in segs:
        for w in (seg.words or []):
            out.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "gain": 0.0})
    return out or None


def analyse(path, sentences, transcribe_audio=False, timed=None):
    """The one call autofilm.py needs: (words, report).

    If the audio can be decoded we use its real speech pockets and RMS. If it cannot (an mp3 on a
    machine without ffmpeg), the file's duration + the script's own timecodes still give exact word
    times; punctuation then stands in for loudness. Nothing silently falls back to made-up timing.
    """
    try:
        audio = read_pcm(path)
        env, step = envelope(audio)
        segs = speech_segments(env, step)
        peak = float(np.percentile(env, 99.5)) or 1e-6
        decoded, duration = True, round(len(audio) / RATE, 3)
    except Exception:
        duration = audio_duration(path)
        env = np.full(max(1, int(duration / WIN)), 0.2, dtype=np.float32)
        step = WIN
        if timed:
            segs = [(float(x["t"]), float(timed[i + 1]["t"]) if i + 1 < len(timed) else duration)
                    for i, x in enumerate(timed)]
            segs = [(a, max(a + 0.2, b)) for a, b in segs]
        else:
            segs = [(0.15, max(0.5, duration - 0.15))]
        peak, decoded = 0.2, False
    words = None
    if transcribe_audio:
        words = transcribe(path)
    if not words:
        words = align_to_script(sentences, segs, env, step=step)
    if not decoded:                                   # no waveform: punctuation marks the accents
        for w in words:
            t = w["w"]
            hot = any(c in t for c in "!?।") or len(t) > 8 or t.isupper()
            w["gain"] = round(peak * (0.95 if hot else 0.42 + 0.16 * (len(t) % 3)), 5)
    elif "gain" not in words[0]:
        for w in words:
            i0, i1 = int(w["s"] / step), max(1, int(w["e"] / step))
            w["gain"] = round(float(np.mean(env[i0:i1])) if i1 > i0 and len(env) else 0.0, 5)
    report = {"audio": os.path.basename(path), "duration": duration,
              "sample_rate": RATE, "speech_segments": [list(x) for x in segs],
              "loudness_peak": round(peak, 5), "waveform_decoded": decoded,
              "words": len(words), "transcribed": bool(words and transcribe_audio)}
    return words, report


def main():
    ap = argparse.ArgumentParser(description="Analyse narration audio into timed words + a loudness map.")
    ap.add_argument("audio", help="wav (direct) or mp3/m4a (needs ffmpeg)")
    ap.add_argument("--script", required=True, help="the script text, or a file with it")
    ap.add_argument("--words", help="write words.json here")
    ap.add_argument("--report", help="write the audio analysis JSON here")
    ap.add_argument("--transcribe", action="store_true", help="use faster-whisper when installed")
    a = ap.parse_args()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from autofilm import split_sentences
    text = a.script
    if os.path.exists(text):
        text = open(text, encoding="utf-8").read()
    sents, timed = parse_timestamped_script(text)
    if not sents:
        sents, timed = split_sentences(text), None
    words, report = analyse(a.audio, sents, a.transcribe, timed=timed)
    if a.words:
        os.makedirs(os.path.dirname(os.path.abspath(a.words)), exist_ok=True)
        json.dump(words, open(a.words, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.report:
        os.makedirs(os.path.dirname(os.path.abspath(a.report)), exist_ok=True)
        json.dump(report, open(a.report, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("audio: %.2f s, %d speech pockets, %d timed words (%s)" %
          (report["duration"], len(report["speech_segments"]), len(words),
           "whisper" if report["transcribed"] else "energy-aligned"))
    if a.words:
        print("words ->", a.words)
    if a.report:
        print("report ->", a.report)


if __name__ == "__main__":
    main()

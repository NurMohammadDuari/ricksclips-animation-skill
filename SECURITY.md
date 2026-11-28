# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| `main` (V1.1+) | ✅ |
| Older commits and V1.0 trees | ❌ |

## Reporting a vulnerability

**Do not open a public issue for security problems.**

Report privately through GitHub's private vulnerability reporting:

<https://github.com/NurMohammadDuari/ricksclips-animation-skill/security/advisories/new>

Please include:

- the affected file, tool or command,
- a minimal reproduction (a small `film.json` or episode if relevant),
- the impact you expect,
- any suggested fix.

You can expect an acknowledgement within **72 hours** and a status update within
**7 days**. Valid reports are fixed, credited unless you prefer to stay
anonymous, and published as an advisory.

## Threat model — read this before running an episode

This pipeline **executes episode code**. A film loads JavaScript set modules
(`episodes/<slug>/sets/*.js`), Python tools and npm packages, and renders them in
a headless browser.

- Treat any episode you did not write as **untrusted code**. Review `sets/`,
  `cast/`, `tools/` and `film.json` before running `render.mjs` or `autofilm.py`.
- `autofilm.py` writes files into the episode folder. Run it in a container or a
  dedicated user account when processing third-party scripts.
- Do not put API keys (Fish Audio, etc.) in `film.json`, episode files or commits.
  Use environment variables.

## In scope

- Arbitrary code execution or path traversal in `tools/` or the render kit.
- Gate bypass: a film that reports 0 FAIL while violating a documented gate.
- Leaked credentials or personal data in the repository.
- Malicious or impersonating download links in the docs.
- Vulnerabilities in the committed `vendor/` code (three.js) that affect users.

## Out of scope

- Vulnerabilities in Node, Python, ffmpeg, Playwright, Blender or three.js —
  report those upstream.
- Running code from an episode you chose to trust.
- Copyright or licence disputes about reference material (see
  [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md)).
- Denial of service caused by intentionally enormous films or frame counts.

## Safe harbour

We will not pursue or support legal action against researchers who make a
good-faith effort to avoid privacy violations and service disruption, only test
accounts and data they own or have permission to use, report privately, and give
us reasonable time to fix the issue before disclosure.

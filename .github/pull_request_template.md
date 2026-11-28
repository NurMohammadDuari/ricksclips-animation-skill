## What does this change?

<!-- One or two sentences. Link the issue: Fixes #123 -->

## Type of change

- [ ] Bug fix
- [ ] New gate
- [ ] New set / pose / cast / camera formula
- [ ] Tool or pipeline improvement
- [ ] Documentation
- [ ] Accessibility improvement
- [ ] Other

## Gate result

<!-- Paste the last lines of `python tools/film_plan.py check <film.json>` -->

```text
FAIL: 0
WARN: ...
```

- [ ] `check` ends with **0 FAIL**.
- [ ] Any accepted WARN has a written reason in that episode's `CAMERA_NOTE.md`.

## How did you verify it?

<!-- Stills (`--frames`), storyboard tiles, an animatic, or a test run. -->

## Checklist

- [ ] I read [CONTRIBUTING.md](../CONTRIBUTING.md) and follow the [Code of Conduct](../CODE_OF_CONDUCT.md).
- [ ] No `node_modules/`, `__pycache__/`, `out/` caches or render temp folders in the diff.
- [ ] No API keys, private audio or personal data.
- [ ] `tools/film_plan.py` stays pure Python (math + json only).
- [ ] Sets and episodes follow `docs/ARCHITECTURE.md` (metres, Z up, `B2T`, `userData.role`).
- [ ] I agree to license this contribution under CC BY 4.0.

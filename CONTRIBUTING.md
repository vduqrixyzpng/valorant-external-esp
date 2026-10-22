# Contributing to valorant-external-esp

Thanks for your interest in this educational research project.

## Scope

This repository exists purely for studying **external process memory reading**
and overlay rendering techniques against Riot's Vanguard-protected client.
Nothing here is a working cheat — offsets are stale by design and features are
intentionally incomplete. Do not submit PRs that "fix" offsets or add working
aimbot logic; those will be closed.

## Ground rules

1. **Educational only.** Every module must carry a docstring explaining *what*
   technique it demonstrates (read-only memory, ImGui overlay, input hooks).
2. **No kernel drivers.** External user-mode only. Kernel components (spoofers,
   hypervisor bypasses) are out of scope.
3. **No Vanguard bypass code.** Discussing Vanguard in docs is fine; shipping
   a bypass is not.
4. **Match the layout.** New feature modules live under
   `valorant_esp/features/`, shared plumbing under `valorant_esp/lib/`.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest tests/
```

## PR checklist

- [ ] Feature lives in the right package folder
- [ ] Added a test stub under `tests/`
- [ ] Ran `pytest` locally
- [ ] Updated `config/default.toml` if new tunables were added
# UWG Registry

This repo is a single public registry for UWG (Universal Walkthrough Generator).

## Contents
- `games/` – per-game entries (PR-friendly).
- `dist/index.json` – generated registry index UWG downloads.
- `plugins/` – plugin zip files referenced by the index (simple hosting for now).
- `schemas/` – JSON Schemas used by CI validation.
- `tools/` – scripts to build/validate the registry.
- `.github/workflows/validate.yml` – CI validation.

## For UWG users
Point UWG at:
- `https://raw.githubusercontent.com/OlaveOyol/UWG-Registry/main/dist/index.json`

## For contributors
1. Add/edit a game entry under `games/<slug>/`.
2. Run `python tools/build_index.py` (writes `dist/index.json`).
3. Run `python tools/validate.py`.
4. Open a PR.

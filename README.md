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

### Key concepts (important)
- **How UWG identifies a game:** UWG computes `gameId = "renpy:" + config.save_directory` at runtime.
- **Registry folder name:** `games/<folder>/` is just an organizing slug for the repo; it does **not** need to match `gameId`.
- **Aliases:** Use `aliases` to match multiple `gameId` strings (old save dirs, common names, older mods, etc.) to the same entry.

### Add a new game (first time)
1. Find the game’s `config.save_directory`:
   - Open the game’s `game/options.rpy` and look for `define config.save_directory = "..."`.
   - The primary `gameId` should be `renpy:<that string>`.
2. Create a new folder: `games/<your_slug>/`
3. Add `games/<your_slug>/game.json`:
   - Set `gameId` to `renpy:<save_directory>`
   - Set `displayName` to the human name
   - Set `saveDirectory` to the raw save dir string (without `renpy:`)
   - Set `aliases` to any other identifiers you want to match (see Aliases section below)
4. Add `games/<your_slug>/plugins.json`:
   - Add one or more plugin entries (usually just one) with `assetUrl` + `sha256`.
   - This repo currently hosts zips under `plugins/` and uses raw GitHub URLs, but releases also work.
5. Build + validate locally:
   - `python tools/build_index.py`
   - `python tools/validate.py`
6. Open a PR.

### Update an existing game (new plugin version)
When the game updates, you’ll usually publish a new plugin zip version.
1. Build the new plugin zip (e.g. `uwg.<game>.walkthrough-1.2.0.zip`).
2. Compute sha256 for the zip and upload it:
   - Option A (simple): commit the zip into `plugins/` in this repo.
   - Option B (recommended long-term): attach the zip to a GitHub Release and use that asset URL.
3. Edit `games/<your_slug>/plugins.json`:
   - Update `version`
   - Update `assetUrl`
   - Update `sha256`
   - Keep old versions only if you explicitly want downgrade support; otherwise replace the entry.
4. Run:
   - `python tools/build_index.py`
   - `python tools/validate.py`
5. Open a PR.

### Aliases (how to use them)
Use `aliases` in `game.json` to handle cases like:
- The developer changes `config.save_directory` between game versions.
- You previously shipped a “friendly” `gameId` but UWG now uses the real one (or vice-versa).
- You want to accept common community naming (`renpy:oppai_odyssey`) even if the real save dir is different.

Guidelines:
- Put the **real current** `gameId` (`renpy:<save_directory>`) in `gameId`.
- Put any previous/alternate identifiers in `aliases`, including:
  - old save dirs: `renpy:<old_save_directory>`
  - community/friendly ids: `renpy:some_name`
- If you add a new alias, it should be treated as “extra matching,” not a new canonical id.

### Notes
- `dist/index.json` is generated; don’t hand-edit it. Always run `python tools/build_index.py`.

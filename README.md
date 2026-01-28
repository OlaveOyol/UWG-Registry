# UWG Registry (test repo)

This is a minimal GitHub-hostable registry repo for UWG.

## Contents
- `dist/index.json` – registry index UWG downloads.
- `plugins/` – plugin zip files referenced by the index.

## How to use (OppaiOdyssey test)
1. Create a GitHub repo and push this folder.
2. Edit `dist/index.json` and replace:
   - `<OWNER>` with your GitHub username/org
   - `<REPO>` with the repo name
3. In the target game, set:
   - `UWG_REGISTRY_INDEX_URL = "https://raw.githubusercontent.com/<OWNER>/<REPO>/main/dist/index.json"`


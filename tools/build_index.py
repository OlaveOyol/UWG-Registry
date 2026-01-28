import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def validate(schema, instance, label: str):
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
    if errors:
        print(f"\nSchema errors in {label}:")
        for err in errors[:50]:
            loc = "/".join(str(p) for p in err.path)
            print(f"  - {loc or '<root>'}: {err.message}")
        raise SystemExit(2)


def main():
    schema_index = load_json(ROOT / "schemas" / "uwg-registry-index.schema.json")
    schema_game = load_json(ROOT / "schemas" / "uwg-registry-game.schema.json")
    schema_plugins = load_json(ROOT / "schemas" / "uwg-registry-plugins.schema.json")

    games_dir = ROOT / "games"
    games = {}

    if not games_dir.exists():
        raise SystemExit("Missing games/ directory")

    for game_folder in sorted([p for p in games_dir.iterdir() if p.is_dir()]):
        if game_folder.name.startswith("_"):
            continue
        game_json = game_folder / "game.json"
        plugins_json = game_folder / "plugins.json"
        if not game_json.exists() or not plugins_json.exists():
            raise SystemExit(f"Missing game.json/plugins.json in {game_folder}")

        game = load_json(game_json)
        plugins = load_json(plugins_json)
        validate(schema_game, game, str(game_json))
        validate(schema_plugins, plugins, str(plugins_json))

        game_id = game["gameId"]
        if plugins["gameId"] != game_id:
            raise SystemExit(f"{plugins_json} gameId must match {game_id!r}")

        games[game_id] = {
            "gameId": game_id,
            "displayName": game["displayName"],
            "saveDirectory": game["saveDirectory"],
            "aliases": game.get("aliases", []),
            "plugins": plugins["plugins"],
        }

    index = {
        "registryVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "games": games,
    }

    validate(schema_index, index, "generated index")
    write_json(ROOT / "dist" / "index.json", index)
    print("Wrote dist/index.json")


if __name__ == "__main__":
    main()


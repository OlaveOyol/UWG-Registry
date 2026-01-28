import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_instance(schema, instance, instance_path: Path):
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        print(f"\nSchema errors in {instance_path}:")
        for err in errors[:50]:
            loc = "/".join(str(p) for p in err.path)
            print(f"  - {loc or '<root>'}: {err.message}")
        raise SystemExit(2)


def main():
    index_schema = load_json(ROOT / "schemas" / "uwg-registry-index.schema.json")
    game_schema = load_json(ROOT / "schemas" / "uwg-registry-game.schema.json")
    plugins_schema = load_json(ROOT / "schemas" / "uwg-registry-plugins.schema.json")

    games_dir = ROOT / "games"
    for game_json in games_dir.rglob("game.json"):
        validate_instance(game_schema, load_json(game_json), game_json)
    for plugins_json in games_dir.rglob("plugins.json"):
        validate_instance(plugins_schema, load_json(plugins_json), plugins_json)

    dist_index = ROOT / "dist" / "index.json"
    if dist_index.exists():
        validate_instance(index_schema, load_json(dist_index), dist_index)

    print("OK")


if __name__ == "__main__":
    main()


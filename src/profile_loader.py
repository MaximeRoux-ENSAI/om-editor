from pathlib import Path

import yaml


def load_profiles(path: Path) -> dict:
    if not path.exists():
        return {}

    with open(path, encoding="utf-8") as file:
        return yaml.safe_load(file) or {}
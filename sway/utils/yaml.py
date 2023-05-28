from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_FILE_PATH = Path("./.sway-config.yaml")


def yaml_load(o: Any, **kwargs: Any):
    return yaml.load(
        o,
        Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader),
        **kwargs,
    )


def yaml_dump(o: Any, **kwargs: Any) -> str:
    return yaml.dump(
        o,
        Dumper=getattr(yaml, "CSafeDumper", yaml.SafeDumper),
        default_flow_style=False,
        indent=4,
        sort_keys=False,
        **kwargs,
    )


def get_config():
    with open(DEFAULT_CONFIG_FILE_PATH) as f:
        manifest = yaml_load(f.read())

    return manifest


def set_config(data: Any) -> None:
    with open(DEFAULT_CONFIG_FILE_PATH, "w") as f:
        f.write(yaml_dump(data))


def touch_config() -> None:
    DEFAULT_CONFIG_FILE_PATH.touch(mode=0o600, exist_ok=True)

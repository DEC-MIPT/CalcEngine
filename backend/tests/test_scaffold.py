import importlib
from pathlib import Path

import app

LAYERS = [
    "api",
    "schemas",
    "models",
    "repositories",
    "services",
    "parameters",
    "engine",
    "reporting",
    "core",
    "db",
    "worker",
]


def test_all_layers_exist_as_packages() -> None:
    app_dir = Path(app.__file__).parent
    for layer in LAYERS:
        assert (app_dir / layer / "__init__.py").is_file()


def test_all_layers_import_without_error() -> None:
    for layer in LAYERS:
        importlib.import_module(f"app.{layer}")

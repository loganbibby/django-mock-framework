import importlib
import pkgutil
from pathlib import Path


def find_modules(path, prefix=None):
    modules = []

    for _, name, is_package in pkgutil.iter_modules([path]):
        if not is_package:
            if prefix:
                modules.append(f"{prefix}.{name}")
            else:
                modules.append(name)
        else:
            modules += find_modules(f"{path}/{name}", prefix=name)

    return modules


def autoloader():
    for path in Path(__file__).resolve(strict=True).parent.iterdir():
        modules = find_modules(path)

        for module in modules:
            importlib.import_module(f"development.mocks.{path.name}.{module}")

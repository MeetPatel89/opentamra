from __future__ import annotations

import importlib
import pkgutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.pipeline.base_step import BaseStep

_STEP_REGISTRY: list[type[BaseStep]] = []
_discovered = False


def register_step(cls: type[BaseStep]) -> type[BaseStep]:
    _STEP_REGISTRY.append(cls)
    return cls


def _discover_steps() -> None:
    global _discovered
    if _discovered:
        return
    from backend.pipeline import steps as steps_pkg

    for _importer, modname, _ispkg in pkgutil.walk_packages(
        steps_pkg.__path__, prefix=steps_pkg.__name__ + "."
    ):
        importlib.import_module(modname)
    _discovered = True


def get_ordered_steps() -> list[BaseStep]:
    _discover_steps()
    steps = [cls() for cls in _STEP_REGISTRY]
    steps.sort(key=lambda s: s.order)
    print("--------------------------------")
    print("Steps Registry:")
    print(_STEP_REGISTRY)
    print("--------------------------------")
    print("Steps:")
    print("--------------------------------")
    print(f"Discovered {len(steps)} steps")
    print(steps)
    print("--------------------------------")
    return steps

import importlib
import logging
import sys
import traceback
from importlib.machinery import SourceFileLoader
from inspect import isclass, isfunction
from pathlib import Path
from types import ModuleType
from typing import Optional

from hotswap.watchdog import Watchdog

LOGGER = logging.getLogger(__name__)


class g:
    lock: bool = False
    watchdog: Optional[Watchdog] = None


def main(func):
    def wrapper(*args, **kwargs):
        if g.lock:
            return
        g.lock = True
        g.watchdog = Watchdog(hotswap)
        g.watchdog.start()
        update_watchdog()
        return func(*args, **kwargs)

    return wrapper


def override(a: object, b: object):
    for x in dir(a):
        if x.startswith("__"):
            continue
        if not hasattr(b, x):
            try:
                delattr(a, x)
            except:
                pass

    for x in dir(b):
        if x.startswith("__"):
            continue
        try:
            attr = getattr(b, x)
            if isfunction(attr):
                # setattr(a, x, attr)
                getattr(a, x).__code__ = attr.__code__

            if isclass(attr):
                if hasattr(b, x):
                    override(getattr(a, x), attr)
        except AttributeError:
            continue


def module_from_path(path: Path) -> Optional[ModuleType]:
    for mod in sys.modules.values():
        if not hasattr(mod, "__file__"):
            continue

        if mod.__file__ is None:
            continue

        if Path(mod.__file__).absolute() != path:
            continue

        return mod

    return None


def hotswap(path: Path) -> None:
    if not path.exists():
        return

    if not path.is_file():
        return

    exist = module_from_path(path.absolute())
    if exist is None:
        return

    spec = importlib.util.spec_from_file_location(path.stem, path)
    if not spec:
        return
    module = importlib.util.module_from_spec(spec)
    loader: SourceFileLoader = spec.loader

    try:
        loader.exec_module(module)
    except Exception as e:
        LOGGER.warning(f"{path} failed to reload")
        LOGGER.warning(traceback.format_exc())
        return
    LOGGER.info(f"{path} reloaded")
    override(exist, module)
    update_watchdog()


def update_watchdog():
    g.watchdog.clear()
    for mod in sys.modules.values():
        if not hasattr(mod, "__file__") or mod.__file__ is None:
            continue
        if not Path(mod.__file__).is_file():
            continue
        g.watchdog.add(Path(mod.__file__))

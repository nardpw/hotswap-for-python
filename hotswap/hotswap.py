import importlib
from importlib.machinery import SourceFileLoader
from inspect import isclass, isfunction
import logging
from pathlib import Path
import sys
from types import ModuleType
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOGGER = logging.getLogger(__name__)


class EventHandler(FileSystemEventHandler):

    def __init__(self, callback) -> None:
        self.callback = lambda e: callback(
            e if isinstance(e, str) else e.src_path
        )
        self.on_modified = self.callback
        self.on_created = self.callback


def module_from_path(filepath: Path) -> Optional[ModuleType]:
    for mod in sys.modules.values():
        if not hasattr(mod, '__file__'):
            continue
        if mod.__file__ is None:
            continue
        if Path(mod.__file__) != filepath:
            continue
        return mod


class g:
    lock: bool = False


def main(func):
    def wrapper(*args, **kwargs):
        if g.lock:
            return
        g.lock = True
        return func(*args, **kwargs)
    return wrapper


def override(a: object, b: object, i=64):
    for x in dir(a):
        if x.startswith('__'):
            continue
        if not hasattr(b, x):
            try:
                delattr(a, x)
            except:
                pass
    for x in dir(b):
        if x.startswith('__'):
            continue
        try:
            attr = getattr(b, x)
            if isfunction(attr):
                setattr(a, x, attr)

            if isclass(attr):
                if i > 0:
                    if hasattr(b, x):
                        override(getattr(a, x), attr, i=i-1)
        except AttributeError:
            continue


def hotswap(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)

    if not spec:
        return

    module = importlib.util.module_from_spec(spec)
    exist = module_from_path(filepath=path.absolute())

    loader: SourceFileLoader = spec.loader

    try:
        loader.exec_module(module)
    except:
        LOGGER.warning(f'failed hot-swapping {path}')
        return

    if exist:
        override(exist, module)


event_handler = EventHandler(lambda x: hotswap(Path(x)))
observer = Observer()
observer.schedule(event_handler, './', recursive=True)
observer.start()

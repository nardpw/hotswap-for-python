from typing import Dict, Callable
from pathlib import Path
from hashlib import sha256
from time import sleep
from threading import Thread


class Watchdog:
    def __init__(self, callback: Callable[[Path], None]):
        self.callback = callback
        self.files: Dict[Path, int] = {}

    def run(self):
        while True:
            self.check()
            sleep(0.1)

    def start(self):
        Thread(target=self.run, daemon=True, name="Watchdog").start()

    def check(self):
        for path, hash in self.files.copy().items():
            if not path.exists():
                self.remove(path)
                continue
            new_hash = self.get_hash(path)
            if new_hash != hash:
                self.callback(path)
                self.files[path] = new_hash

    def get_hash(self, path: Path):
        return int(sha256(path.read_bytes()).hexdigest(), 16)

    def add(self, path: Path):
        self.files[path] = self.get_hash(path)

    def remove(self, path: Path):
        del self.files[path]

    def clear(self):
        self.files.clear()

from typing import Any


class TextFileIoManager:
    def __init__(self) -> None:
        self._valid_suffixes: set[str] = {".txt"}

    @property
    def valid_suffixes(self) -> set[str]:
        return self._valid_suffixes

    def is_valid(self, file: Any) -> bool:
        return any(suffix in self._valid_suffixes for suffix in self._valid_suffixes)

    def read_file(self, file: Any) -> str:
        return file.read() or {}


singleton = TextFileIoManager()

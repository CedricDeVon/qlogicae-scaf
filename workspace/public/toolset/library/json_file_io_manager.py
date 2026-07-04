import json
from typing import Any


class JsonFileIoManager:
    def __init__(self) -> None:
        self._valid_suffixes: set[str] = {".json"}

    @property
    def valid_suffixes(self) -> set[str]:
        return self._valid_suffixes

    def is_valid(self, file: Any) -> bool:
        return any(suffix in self._valid_suffixes for suffix in self._valid_suffixes)

    def read_file(self, file: Any) -> Any:
        return json.load(file) or {}


singleton = JsonFileIoManager()

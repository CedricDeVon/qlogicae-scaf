import re
from typing import Any
from collections.abc import Mapping


class MacrosManager:
    def __init__(self) -> None:
        self.pattern = re.compile(r"\$\{\{\s*([A-Za-z0-9._-]+)\s*\}\}")

    def resolve_many(self, values: Any) -> Mapping[str, Any]:
        cache = {}

        return {key: self.resolve_one(key, values, cache, set()) for key in values}

    def resolve_one(self, key: Any, values: Any, cache: Any, stack: Any) -> str:
        if key in cache:
            return cache[key]

        if key in stack:
            raise Exception(f"'{key}' is a circular reference")

        if key not in values:
            raise Exception(f"'{key}' is an unknown macros")

        stack.add(key)

        value = values[key]

        if not isinstance(value, str):
            cache[key] = value
            stack.remove(key)
            return value

        def handle_parse_one(match):
            referenced_key = match.group(1)

            return self.resolve_one(referenced_key, values, cache, stack)

        resolved = self.pattern.sub(handle_parse_one, value)

        stack.remove(key)

        cache[key] = resolved

        return resolved

    def parse_many(self, values: Any, resolved: Any) -> str:
        return self.parse_one(values, resolved)

    def parse_one(self, value: str, resolved: Any) -> str:
        if isinstance(value, str):
            return self.pattern.sub(
                lambda match: resolved.get(match.group(1), match.group(0)),
                value,
            )

        if isinstance(value, dict):
            return {
                key: self.parse_one(child, resolved) for key, child in value.items()
            }

        if isinstance(value, list):
            return [self.parse_one(child, resolved) for child in value]

        if isinstance(value, tuple):
            return tuple(self.parse_one(child, resolved) for child in value)

        if isinstance(value, set):
            return {self.parse_one(child, resolved) for child in value}

        return value


singleton = MacrosManager()

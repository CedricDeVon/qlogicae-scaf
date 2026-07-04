from typing import Any
from collections.abc import Mapping


class ValueCacheStorageManager:
    def __init__(self) -> None:
        self._collection: Mapping[str, Any] = {}

    @property
    def collection(self) -> Mapping[str, Any]:
        return self._collection

    def is_key_found(self, keys: list[str]) -> bool:
        if not keys:
            return False

        cache = self._collection

        for key in keys:
            if isinstance(cache, dict):
                if key not in cache:
                    return False

            elif isinstance(cache, (list, tuple)):
                if not isinstance(key, int):
                    return False

                if key < 0 or key >= len(cache):
                    return False

            else:
                return False

            cache = cache[key]

        return True

    def get_one_value(self, keys: list[str]) -> Any:
        if not keys:
            return None

        cache = self._collection

        for key in keys:
            if isinstance(cache, dict):
                if key not in cache:
                    return None

            elif isinstance(cache, (list, tuple)):
                if not isinstance(key, int):
                    return None

                if key < 0 or key >= len(cache):
                    return None

            else:
                return None

            cache = cache[key]

        return cache

    def set_one_value(
        self,
        keys: list[str],
        value: Any,
        create_missing: bool = True,
    ) -> bool:
        if not keys:
            raise ValueError("'keys' cannot be empty")

        cache = self._collection

        for key in keys[:-1]:
            if isinstance(cache, dict):
                if key not in cache:
                    if not create_missing:
                        raise KeyError(f"key '{key}' not found")

                elif not isinstance(cache[key], (dict, list)):
                    raise TypeError(
                        f"key '{key}' does not reference a dictionary or list"
                    )

                cache = cache[key]

            elif isinstance(cache, list):
                if not isinstance(key, int):
                    raise TypeError(f"expected an index, got '{type(key).__name__}'")

                if key < 0 or key >= len(cache):
                    raise IndexError(f"index '{key}' is out of range")

                cache = cache[key]

            else:
                raise TypeError(f"cannot traverse into '{type(cache).__name__}'")

        last = keys[-1]

        if isinstance(cache, dict):
            cache[last] = value

        elif isinstance(cache, list):
            if not isinstance(last, int):
                raise TypeError(f"expected an index, got {type(last).__name__}")

            if last < 0 or last >= len(cache):
                raise IndexError(f"index '{last}' is out of range")

            cache[last] = value

        else:
            raise TypeError("Destination is neither a dictionary nor a list")

    def remove_one_value(self, keys: list[str]) -> bool:
        if not keys:
            raise ValueError("keys cannot be empty")

        cache = self._collection

        for key in keys[:-1]:
            if isinstance(cache, dict):
                if key not in cache:
                    raise KeyError(f"key '{key}' not found")

            elif isinstance(cache, list):
                if not isinstance(key, int):
                    raise TypeError(f"expected an index, got {type(key).__name__}")

                if key < 0 or key >= len(cache):
                    raise IndexError(f"index '{key}' is out of range")

            else:
                raise TypeError(f"cannot traverse into '{type(cache).__name__}'")

            cache = cache[key]

        last = keys[-1]

        if isinstance(cache, dict):
            try:
                del cache[last]
            except KeyError:
                raise KeyError(f"key '{last}' not found") from None

        elif isinstance(cache, list):
            if not isinstance(last, int):
                raise TypeError(f"expected an index, got {type(last).__name__}")

            if last < 0 or last >= len(cache):
                raise IndexError(f"index '{last}' is out of range")

            del cache[last]

        else:
            raise TypeError("destination is neither a dictionary nor a list")

    def clear_all_values(self) -> bool:
        self._collection.clear()

        return True

    def display_one_item(self, key: str) -> bool:
        print(f"- {key}: {self._collection[key]}")

        return True

    def display_all_items(self) -> bool:
        for item in self._collection.items():
            self.display_one_item(item[0])

        return True


singleton = ValueCacheStorageManager()

from typing import Any

from pympler import asizeof


class ObjectMemoryBenchmarkManager:
    def evalaute_value(self, value: Any) -> int:
        return asizeof.asizeof(value)


singleton = ObjectMemoryBenchmarkManager()

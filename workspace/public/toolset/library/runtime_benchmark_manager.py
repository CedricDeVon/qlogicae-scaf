import time
from typing import Any


class RuntimeBenchmarkManager:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0

    def start(self) -> bool:
        self.start_time = time.time_ns()

        return True

    def stop(self) -> bool:
        self.stop_time = time.time_ns()

        return True

    def get_duration_in_nanoseconds(self) -> int:
        return self.stop_time - self.start_time


singleton = RuntimeBenchmarkManager()

import tracemalloc


class MemoryAllocationBenchmarkManager:
    def __init__(self) -> None:
        self.started = False
        self.snapshot = None

    def start_execution(self, frame_count: int = 25) -> None:
        if self.started:
            return

        tracemalloc.start(frame_count)
        self.started = True

    def stop_execution(self) -> None:
        if not self.started:
            return

        tracemalloc.stop()
        self.started = False
        self.snapshot = None

    def clear_results(self) -> None:
        tracemalloc.clear_traces()

    def reset_peak(self) -> None:
        tracemalloc.reset_peak()

    def current_memory(self) -> int:
        current, _ = tracemalloc.get_traced_memory()
        return current

    def peak_memory(self) -> int:
        _, peak = tracemalloc.get_traced_memory()
        return peak

    def take_snapshot(self) -> None:
        self.snapshot = tracemalloc.take_snapshot()

    def compare_to_snapshot(
        self,
        key_type: str = "lineno",
    ):
        if self.snapshot is None:
            raise RuntimeError("no snapshot has been taken yet")

        current = tracemalloc.take_snapshot()

        return current.compare_to(
            self.snapshot,
            key_type,
        )

    def get_statistics(
        self,
        key_type: str = "lineno",
    ):
        snapshot = tracemalloc.take_snapshot()

        return snapshot.statistics(key_type)

    def save_snapshot(
        self,
        filename: str,
    ) -> None:
        snapshot = tracemalloc.take_snapshot()
        snapshot.dump(filename)

    def load_snapshot(
        self,
        filename: str,
    ):
        return tracemalloc.Snapshot.load(filename)

    def __enter__(self):
        self.start_execution()
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):
        self.stop_execution()


singleton = MemoryAllocationBenchmarkManager()

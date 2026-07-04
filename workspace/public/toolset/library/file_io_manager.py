class FileIoManager:
    def __init__(self) -> None:
        self._file_encoding: str = "utf-8"

    @property
    def file_encoding(self) -> set[str]:
        return self._file_encoding


singleton = FileIoManager()

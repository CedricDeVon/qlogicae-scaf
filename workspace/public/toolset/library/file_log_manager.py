import queue
import logging
from pathlib import Path
from logging.handlers import QueueHandler, QueueListener

from library.log_format import LogFormat
from library.log_options import LogOptions


class FileLogManager:
    def __init__(self) -> None:
        self.logger = logging.getLogger("file-logger")

        self.logger.setLevel(logging.DEBUG)

        self.logger.propagate = False

        self.logger.handlers.clear()

        self.file_handlers = {}

        self.log_queue = queue.Queue()

        self.queue_handler = QueueHandler(self.log_queue)

        self.logger.addHandler(self.queue_handler)

        self.listener = QueueListener(self.log_queue)

        self.listener.start()

    def log(self, message: str, options: LogOptions = LogOptions()) -> str:
        if not options.is_enabled:
            return message

        self.logger.log(options.log_level, message, stacklevel=options.stack_level)

        return message

    def log_debug(
        self,
        message: str,
        options: LogOptions = LogOptions(log_level=logging.DEBUG),
    ) -> str:
        return self.log(message, options)

    def log_info(
        self,
        message: str,
        options: LogOptions = LogOptions(log_level=logging.INFO),
    ) -> str:
        return self.log(message, options)

    def log_warning(
        self,
        message: str,
        options: LogOptions = LogOptions(log_level=logging.WARNING),
    ) -> str:
        return self.log(message, options)

    def log_error(
        self,
        message: str,
        options: LogOptions = LogOptions(log_level=logging.ERROR),
    ) -> str:
        return self.log(message, options)

    def log_critical(
        self,
        message: str,
        options: LogOptions = LogOptions(log_level=logging.CRITICAL),
    ) -> str:
        return self.log(message, options)

    def rebuild_listener(self) -> bool:
        self.listener.stop()

        self.listener = QueueListener(self.log_queue, *self.file_handlers.values())

        self.listener.start()

        return True

    def add_file_output(self, file_path: str) -> bool:
        path = Path(file_path).resolve()

        if path in self.file_handlers:
            return False

        path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(path, encoding="utf-8")

        handler.setFormatter(LogFormat())

        self.file_handlers[path] = handler

        self.rebuild_listener()

        return True

    def remove_file_output(self, file_path: str) -> bool:
        path = Path(file_path).resolve()

        handler = self.file_handlers.get(path)

        if handler is None:
            return False

        handler.close()

        del self.file_handlers[path]

        self.rebuild_listener()

        return True

    def clear_file_outputs(self) -> bool:
        for handler in self.file_handlers.values():
            handler.close()

        self.file_handlers.clear()

        self.rebuild_listener()

        return True

    def shutdown(self) -> bool:
        self.listener.stop()

        for handler in self.file_handlers.values():
            handler.close()

        self.file_handlers.clear()

        return True


singleton = FileLogManager()

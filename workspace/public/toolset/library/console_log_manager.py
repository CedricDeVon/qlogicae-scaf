import logging

from library.log_format import LogFormat
from library.log_options import LogOptions


class ConsoleLogManager:
    def __init__(self) -> None:
        self.logger = logging.getLogger("console-logger")

        self.logger.setLevel(logging.DEBUG)

        self.logger.propagate = False

        self.logger.handlers.clear()

        handler = logging.StreamHandler()

        handler.setFormatter(LogFormat())

        self.logger.addHandler(handler)

    def log(self, message: str, options: LogOptions = LogOptions()) -> str:
        if not options.is_enabled:
            return

        if options.is_verbose:
            self.logger.log(
                options.log_level,
                message,
                stacklevel=options.stack_level,
            )
        else:
            print(message)

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


singleton = ConsoleLogManager()

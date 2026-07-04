import logging

from library.log_options import LogOptions
from library import console_log_manager, file_log_manager


class LogManager:
    def log(
        self,
        message: str,
        console_options: LogOptions = LogOptions(is_verbose=False),
        file_options: LogOptions = LogOptions(),
    ) -> str:
        console_log_manager.singleton.log(
            message,
            LogOptions(
                is_enabled=console_options.is_enabled,
                is_verbose=console_options.is_verbose,
                log_level=console_options.log_level,
                stack_level=console_options.stack_level + 1,
            ),
        )

        file_log_manager.singleton.log(
            message,
            LogOptions(
                is_enabled=file_options.is_enabled,
                is_verbose=file_options.is_verbose,
                log_level=file_options.log_level,
                stack_level=file_options.stack_level + 1,
            ),
        )

        return message

    def log_debug(
        self,
        message: str,
        console_options: LogOptions = LogOptions(
            log_level=logging.DEBUG, is_verbose=False
        ),
        file_options: LogOptions = LogOptions(log_level=logging.DEBUG),
    ) -> str:
        return self.log(message, console_options, file_options)

    def log_info(
        self,
        message: str,
        console_options: LogOptions = LogOptions(
            log_level=logging.INFO, is_verbose=False
        ),
        file_options: LogOptions = LogOptions(log_level=logging.INFO),
    ) -> str:
        return self.log(message, console_options, file_options)

    def log_warning(
        self,
        message: str,
        console_options: LogOptions = LogOptions(
            log_level=logging.WARNING, is_verbose=False
        ),
        file_options: LogOptions = LogOptions(log_level=logging.WARNING),
    ) -> str:
        return self.log(message, console_options, file_options)

    def log_error(
        self,
        message: str,
        console_options: LogOptions = LogOptions(
            log_level=logging.ERROR, is_verbose=False
        ),
        file_options: LogOptions = LogOptions(log_level=logging.ERROR),
    ) -> str:
        return self.log(message, console_options, file_options)

    def log_critical(
        self,
        message: str,
        console_options: LogOptions = LogOptions(
            log_level=logging.CRITICAL, is_verbose=False
        ),
        file_options: LogOptions = LogOptions(log_level=logging.CRITICAL),
    ) -> str:
        return self.log(message, console_options, file_options)

    def shutdown(self):
        file_log_manager.singleton.shutdown()

        return True


singleton = LogManager()

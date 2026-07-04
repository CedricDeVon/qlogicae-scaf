import logging

from library import timestamp_manager


class LogFormat(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return (
            f"[ {timestamp_manager.singleton.generate_standard_timestamp()} ] "
            f"[ {record.levelname} ] "
            f"{record.getMessage()}"
        )

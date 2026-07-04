import logging
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LogOptions:
    is_enabled: bool = True
    is_verbose: bool = True
    log_level: int = logging.DEBUG
    stack_level: int = 2

import time
from typing import Optional

# Warn: dearlog must be your first import
REFTIME: float = time.monotonic()
"""Instant the program started, means nothing alone"""

__version__: str = "0.1.0"
__author__:  str = "Tremeschin"
__about__:   str = "🪵 A Human Logging Library"

# ---------------------------------------------------------------------------- #

import functools
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager, nullcontext
from datetime import datetime

from attrs import Factory, define


@define
class DearLevel:
    no: int = 50
    name: str = "LEVEL"
    color: str = ""
    extra: dict = Factory(dict)

@define
class DearEvent:

    level: int = 50
    """Verbosity level of the event"""

    date: datetime = Factory(datetime.now)
    """Absolute time the event happened since unix epoch"""

    time: float = Factory(lambda: time.monotonic() - REFTIME)
    """Relative time the event happened since program start"""

    echo: bool = True
    """Whether to echo the message to stdout/stderr"""

# ---------------------------------------------------------------------------- #

@define
class DearHandler(ABC):

    format: str = "{message}"
    """Format string for log messages"""

    @abstractmethod
    def handle(self, event: DearEvent) -> None:
        ...

# ------------------------------------ #

class StdoutHandler(DearHandler):

    rich: bool = True
    """Whether to use rich formatting or plain text"""

    def handle(self, event: DearEvent) -> None:
        ...

# ------------------------------------ #

class StderrHandler(DearHandler):

    rich: bool = True
    """Whether to use rich formatting or plain text"""

    def handle(self, event: DearEvent) -> None:
        ...

# ------------------------------------ #

class FileHandler(DearHandler):
    ...

# ---------------------------------------------------------------------------- #

@define
class DearLogger:

    handlers: list[DearHandler] = Factory(list)
    """Collection of handlers to process records"""

    lock: AbstractContextManager = Factory(nullcontext)
    """Ordering for concurrent logging"""

    level: int = 50
    """Minimum level to log"""

    # Singleton implementation
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance__"):
            self = super().__new__(cls)
            cls.__instance__ = self
        return cls.__instance__

    def thread_safe(self):
        """Guarantee multiline ordering"""
        from threading import Lock
        self.lock = Lock()

    # -------------------------------- #

    def add_level(self, level: DearLevel) -> None:
        self.levels[level.no] = level

    def get_level(self, no: int) -> Optional[DearLevel]:
        return self.levels.get(no, None)

    # -------------------------------- #

    def log(self,
        *args,
        echo: bool=True,
        **kwargs: dict,
    ) -> str:

        # Make message from
        message: str = " ".join(map(str, args))

        # event: DearEvent = DearEvent(
        #     message

        with self.lock:
            for line in message.splitlines():
                for handler in self.handlers:
                    handler.handle(line)
        ...

    @functools.wraps(log)
    def info(self, *args, **kwargs) -> str:
        return self.log(*args, **kwargs, level=50)

logger: DearLogger = DearLogger()
"""Global singleton logger instance"""

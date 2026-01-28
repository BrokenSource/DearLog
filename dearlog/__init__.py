import time

# Warn: dearlog must be your first import
REFTIME: float = time.monotonic()
"""Instant the program started, means nothing alone"""

__version__: str = "0.1.0"
__author__:  str = "Tremeschin"
__about__:   str = "🪵 A Human Logging Library"

# ---------------------------------------------------------------------------- #

import functools
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from attrs import Factory, define


@define
class LogLevel:
    name: str = "LEVEL"
    color: str = ""
    extra: dict = Factory(dict)
    enabled: bool = True


class Levels:
    """See docstrings on logging methods in the main class"""
    TRACE: LogLevel = LogLevel(name="trace", color="dark_turquoise", enabled=False)
    DEBUG: LogLevel = LogLevel(name="debug", color="turquoise4", enabled=False)

    INFO:  LogLevel = LogLevel(name="info",  color="bright_white")
    NOTE:  LogLevel = LogLevel(name="note",  color="bright_blue")
    OK:    LogLevel = LogLevel(name="ok",    color="green")

    MINOR: LogLevel = LogLevel(name="minor", color="grey42")
    SKIP:  LogLevel = LogLevel(name="skip",  color="grey42")
    TODO:  LogLevel = LogLevel(name="todo",  color="dark_blue")
    TIP:   LogLevel = LogLevel(name="tip",   color="dark_cyan")

    FIXME: LogLevel = LogLevel(name="fixme", color="bright_red")
    WARN:  LogLevel = LogLevel(name="warn",  color="yellow")
    ERROR: LogLevel = LogLevel(name="error", color="red")
    CRIT:  LogLevel = LogLevel(name="crit",  color="red")

# ---------------------------------------------------------------------------- #

@define(frozen=True)
class LogEntry:
    """An event that happened and shall be logged"""

    level: LogLevel = None
    """Verbosity level of the event"""

    args: tuple = Factory(tuple)
    """Direct arguments sent"""

    kwargs: dict = Factory(dict)
    """Keyword arguments sent"""

    date: datetime = Factory(datetime.now)
    """Absolute time the event happened (local timezone)"""

    time: float = Factory(lambda: time.monotonic() - REFTIME)
    """Relative time the event happened since program start"""

    echo: bool = True
    """Whether to echo the message to stdout/stderr"""

class LogFormat(str):
    Simple    = "{message}"
    Stopwatch = "[{time:6.3f}] ({level.name:5}) {message}"

# ---------------------------------------------------------------------------- #

@define
class DearHandler(ABC):

    format: str = LogFormat.Stopwatch
    """Format string for log messages"""

    def _format(self, entry: LogEntry) -> str:
        return self.format.format(
            time=entry.time,
            date=entry.date,
            level=entry.level,
            message=" ".join(str(arg) for arg in entry.args),
            **entry.kwargs,
        )
        ...

    @abstractmethod
    def handle(self, entry: LogEntry) -> None:
        ...

# ------------------------------------ #

@define
class StdoutHandler(DearHandler):

    rich: bool = True
    """Whether to use rich formatting or plain text"""

    def handle(self, event: LogEntry) -> None:
        print(self._format(event))

# ------------------------------------ #

@define
class StderrHandler(DearHandler):

    rich: bool = True
    """Whether to use rich formatting or plain text"""

    def handle(self, entry: LogEntry) -> None:
        raise NotImplementedError

# ------------------------------------ #

@define
class FileHandler(DearHandler):
    path: Path = None
    mode: str = "a"

    def __attrs_post_init__(self) -> None:
        self._file = open(self.path, self.mode)

    def handle(self, entry: LogEntry) -> None:
        raise NotImplementedError
        # self._file.write(message + "\n")
        # self._file.flush()

# ---------------------------------------------------------------------------- #

class _Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance__"):
            self = super().__new__(cls)
            cls.__instance__ = self
        return cls.__instance__

@define
class DearLogger(_Singleton):
    """
    A human-friendly logging library.

    Note: Usage docstrings aren't strict, use your best judgement and taste.
    """

    handlers: list[DearHandler] = Factory(list)
    """Collection of handlers to process records"""

    def parse_loglevel(self, config: str) -> None:
        """
        Parse a configuration string for loglevels (case-insensitive).

        Examples:
        - `info`: Enables all levels up to and including info
        - `+all`: Enable all levels
        - `-all,+warn`: Only enable the warn level
        """
        for token in config.split(","):
            raise NotImplementedError

    # -------------------------------- #

    def log(self,
        *args: str,
        _level: LogLevel,
        **kwargs: dict,
    ) -> str:
        """The main, and only one, logging method."""

        # Must be enabled
        if not _level.enabled:
            return ""

        # Issue a log entry
        entry = LogEntry(
            args=args,
            kwargs=kwargs,
            level=_level,
        )

        # Guarantee message order across handlers
        # Fixme: Should be a FIFO per handler
        for handler in self.handlers:
            handler.handle(entry)

    # -------------------------------- #
    # Debugging

    @functools.wraps(log)
    def trace(self, *args, **kwargs) -> None:
        """
        Very detailed events, noisy and high volume. Intentionally doesn't
        return formatted messages unless logged, opt-in by default.

        Examples:
        - `"Resizing ShaderTexture {self.uuid} to {width}x{height}"`
        - `"Calling {type(self).__name__}.update() with {dt=:.4f}s"`
        """
        if Levels.TRACE.enabled:
            return self.log(*args, **kwargs, _level=Levels.TRACE)

    @functools.wraps(log)
    def debug(self, *args, **kwargs) -> None:
        """
        Detailed events near hot paths for diagnostic. Intentionally doesn't
        return formatted messages unless logged, opt-in by default.

        Examples:
        - `"Exported environment variables: {self.environ}"`
        - `"Loaded dictionary from pyproject.toml: {data}"`
        """
        if Levels.DEBUG.enabled:
            return self.log(*args, **kwargs, _level=Levels.DEBUG)

    # -------------------------------- #
    # Nominal

    @functools.wraps(log)
    def info(self, *args, **kwargs) -> str:
        """
        Regular informational messages about events or states, nothing out of
        the ordinary. Should not log actions or decisions that impact flow.

        Examples:
        - `"Finished rendering video file ({output})"`
        - `"OpenGL Renderer: {self.opengl.info['GL_RENDERER']}"`
        """
        return self.log(*args, **kwargs, _level=Levels.INFO)

    @functools.wraps(log)
    def note(self, *args, **kwargs) -> LogLevel:
        """
        Noteworthy events that _may_ require user attention or cause errors,
        and/or actions taken to prevent them or improve user experience.

        Examples:
        - `"Enabling cargo-zigbuild for easier cross-compilation"` (decision)
        - `"You may opt-out of it with AUTO_ZIGBUILD=0"` (advice)
        - `"Audio path ({file}) doesn't exist, using silent audio"` (event)
        - `"PyTorch nightly may be unstable and need updated drivers"` (advice)
        """
        return self.log(*args, **kwargs, _level=Levels.NOTE)

    @functools.wraps(log)
    def ok(self, *args, **kwargs) -> LogLevel:
        """
        Successful operations, checks, basically a shorter "success"

        Examples:
        - `"Compiled binary at ({release})"`
        - `"Finished rendering video ({output})"
        """
        return self.log(*args, **kwargs, _level=Levels.OK)

    # -------------------------------- #
    # Utils

    @functools.wraps(log)
    def minor(self, *args, **kwargs) -> LogLevel:
        """
        Low-importance events that can be safely ignored in most cases, or
        that are echoing items/states for user awareness.

        Examples:
        - `"Loading depth-estimation from cache"`
        - `"• Asset: ({name})` (bundle loop)
        """
        return self.log(*args, **kwargs, _level=Levels.MINOR)

    @functools.wraps(log)
    def skip(self, *args, **kwargs) -> LogLevel:
        """
        Events where an action was intentionally skipped or not performed.

        Examples:
        - `"Skip calling {command}"`
        - `"Already downloaded file at ({path})"`
        """
        return self.log(*args, **kwargs, _level=Levels.SKIP)

    @functools.wraps(log)
    def todo(self, *args, **kwargs) -> LogLevel:
        """
        For unimplemented features, planned actions, or future improvements,
        which shouldn't/may cause disruptions, that would be nice to have.

        Examples:
        - `"Multithreading contexts are not yet supported, locking usage"`
        - `"FFmpeg isn't automatically managed, please have it externally"`
        """
        return self.log(*args, **kwargs, _level=Levels.TODO)

    @functools.wraps(log)
    def tip(self, *args, **kwargs) -> LogLevel:
        """
        Missable or uncommon knowledge to improve user experience.

        Examples:
        - `"(macOS) Use PYTORCH_ENABLE_MPS_FALLBACK=1 to enable CPU fallback"`
        - `"Find your host with 'rustc --version --verbose'"`
        """
        return self.log(*args, **kwargs, _level=Levels.TIP)

    # -------------------------------- #
    # Danger

    @functools.wraps(log)
    def fixme(self, *args, **kwargs) -> LogLevel:
        """
        Tell missing features, potential improvements, or less-than-ideal stuff.

        Must not directly cause Exceptions (`raise` it instead), and should be
        actionable by the user via workarounds, configurations.

        You may use it as "this is knowingly broken" too.

        Examples:
        - `"Cross compilation to macOS needs setting SDKROOT"`
        - `"Files from docker volumes may be owned by root user"`
        """
        return self.log(*args, **kwargs, _level=Levels.FIXME)

    @functools.wraps(log)
    def warn(self, *args, **kwargs) -> LogLevel:
        """
        Potentially harmful situations, undesired states, or recoverable issues.

        Examples:
        - `"Rust doesn't guarantee a working build for Tier 2 target {target}"`
        - `"This model is licensed under CC BY-NC 4.0 (non-commercial)"`
        """
        return self.log(*args, **kwargs, _level=Levels.WARN)

    @functools.wraps(log)
    def error(self, *args, **kwargs) -> LogLevel:
        """
        Error events that _might_ still allow the application to continue
        running, or that require user intervention (externally, code).

        Examples:
        - `"Failed to download file from {url}: {error}, retrying.."`
        - `"Received wrong download size for {file}, redownloading.."`
        - `"Cannot symlink on Windows without Developer Mode enabled"`
        """
        return self.log(*args, **kwargs, _level=Levels.ERROR)

    @functools.wraps(log)
    def crit(self, *args, **kwargs) -> LogLevel:
        """
        Cannot continue running: unrecoverable states, unsupported operations,
        or impossible support for the current hardware/environment, etc.

        Examples:
        - `"Failed to create OpenGL context, ensure you have EGL available"`
        - `"Only Nvidia GPUs are supported in nvibrant"`
        - `"Failed to allocate {size} of GPU memory"`
        """
        return self.log(*args, **kwargs, _level=Levels.CRIT)

logger: DearLogger = DearLogger()
"""Global singleton logger instance"""

# Add default stdout handler
logger.handlers.append(StdoutHandler())

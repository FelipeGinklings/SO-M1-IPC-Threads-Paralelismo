"""Shared data models and operation constants for sender/worker communication."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageMetadata:
    """Container for image dimensions, intensity range, and raw pixel bytes."""

    height: int
    width: int
    maxv: int
    data: bytes

    def to_dict(self):
        """Return only JSON-serializable metadata sent through the pipe header."""
        return {
            "width": self.width,
            "height": self.height,
            "maxv": self.maxv,
        }

    def __str__(self):
        """Return a compact human-readable summary for logs/debugging."""
        return f"height: {self.height}, width: {self.width}, maxv: {self.maxv}"


@dataclass
class Header:
    """Operation configuration provided by sender and consumed by worker."""

    mode: int
    slice_range: tuple[int, int]
    colored: bool = False

    def to_dict(self):
        """Serialize operation parameters so they can be sent as JSON."""
        return {
            "mode": self.mode,
            "slice_range": self.slice_range,
            "colored": self.colored,
        }

    def __str__(self):
        """Return a compact representation of selected operation settings."""
        return f"mode: {self.mode}, slice_range: {self.slice_range}"


# FIFO path used for sender -> worker IPC.
PIPE_PATH = "/tmp/my_pipe"
# Processing modes shared by sender and worker.
NEG_MODE = 0
SLICE_MODE = 1

from dataclasses import dataclass


@dataclass(frozen=True)
class ImageMetadata:
    height: int
    width: int
    maxv: int
    data: bytes

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "maxv": self.maxv,
        }

    def __str__(self):
        return f"height: {self.height}, width: {self.width}, maxv: {self.maxv}"


@dataclass
class Header:
    mode: int
    slice_range: tuple[int, int]
    colored: bool = False

    def to_dict(self):
        return {
            "mode": self.mode,
            "slice_range": self.slice_range,
            "colored": self.colored,
        }

    def __str__(self):
        return f"mode: {self.mode}, slice_range: {self.slice_range}"


PIPE_PATH = "/tmp/my_pipe"
NEG_MODE = 0
SLICE_MODE = 1

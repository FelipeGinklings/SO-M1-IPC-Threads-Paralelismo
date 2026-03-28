from dataclasses import dataclass


@dataclass(frozen=True)
class PGM:
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


PIPE_PATH = "/tmp/my_pipe"
IMAGE_NAME = "horse.ppm"

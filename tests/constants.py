from dataclasses import dataclass


@dataclass(frozen=True)
class PGM:
    height: int
    width: int
    maxv: int

    def __str__(self):
        return f"height: {self.height}, width: {self.width}, maxv: {self.maxv}"


PIPE_PATH = "/tmp/my_pipe"

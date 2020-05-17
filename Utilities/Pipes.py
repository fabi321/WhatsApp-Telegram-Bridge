from io import open
from os import pipe, write, fdopen
from typing import Dict


class Pipes:
    pipes: Dict[str, int] = {}

    def __init__(self, descriptor: str):
        r, w = pipe()
        self.read_pipe: open = fdopen(r)
        self.pipes[descriptor] = w

    def send(self, descriptor: str, data: str):
        data += '\n'
        write(self.pipes[descriptor], data.encode())

    def receive(self) -> str:
        return self.read_pipe.readline()[:-1]

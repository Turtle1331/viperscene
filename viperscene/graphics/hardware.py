from typing import Any

import sys

from viperscene.components import MaterialComponent

class Framebuffer:
    def __init__(self, width: int) -> None:
        assert width >= 0
        self.width = width
        self.buffer = ["%"] * width

    def set_pixel(self, index: int, material: MaterialComponent) -> None:
        assert 0 <= index < self.width
        assert isinstance(material, MaterialComponent)
        self.buffer[index] = material.material

    def clear(self, material: str) -> None:
        assert isinstance(material, str) and len(material) == 1
        self.buffer[:] = [material] * self.width

    def output(self) -> str:
        return "".join(self.buffer)


class Display:
    PERMITTED_CHARS = set( "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`~-_=+[]{}\\|'\";:,.<>/? ")

    def __init__(self, width: int) -> None:
        assert width >= 0
        self.width = width

    def __enter__(self) -> 'Display':
        return self

    def submit_frame(self, framebuffer: Framebuffer) -> None:
        assert framebuffer.width == self.width
        output = framebuffer.output()
        assert set(output) <= self.PERMITTED_CHARS
        print(output, end="\r")
        sys.stdout.flush()

    def __exit__(self, *_: Any) -> None:
        print()

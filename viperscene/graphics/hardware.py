from typing import Any

import sys

from viperscene.components import MaterialComponent


class Framebuffer:
    def __init__(self, width: int) -> None:
        if width < 0:
            raise ValueError(f"Framebuffer cannot have negative width {width}")
        self.width = width
        self.buffer = ["%"] * width

    def set_pixel(self, index: int, material: MaterialComponent) -> None:
        if not 0 <= index < self.width:
            raise ValueError(
                f"Expected pixel index between 0 and {self.width - 1}, got {index}"
            )
        self.buffer[index] = material.material

    def clear(self, material: MaterialComponent) -> None:
        self.buffer[:] = [material.material] * self.width

    def output(self) -> str:
        return "".join(self.buffer)


class Display:
    PERMITTED_CHARS = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`~-_=+[]{}\\|'\";:,.<>/? "
    )

    def __init__(self, width: int) -> None:
        if width < 0:
            raise ValueError(f"Display cannot have negative width {width}")
        self.width = width

    def __enter__(self) -> "Display":
        return self

    def submit_frame(self, framebuffer: Framebuffer) -> None:
        if framebuffer.width != self.width:
            raise ValueError(
                f"Submitted framebuffer width {framebuffer.width} does not equal display width {self.width}"
            )
        output = framebuffer.output()
        if not set(output) <= self.PERMITTED_CHARS:
            raise ValueError(
                f"Non-displayable character(s) in framebuffer: {output - self.PERMITTED_CHARS}"
            )
        print(output, end="\r")
        sys.stdout.flush()

    def __exit__(self, *_: Any) -> None:
        print()

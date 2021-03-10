import sys

from viperscene.components import MaterialComponent

class Framebuffer(object):
    def __init__(self, width):
        assert width >= 0
        self.width = width
        self.buffer = ["%"] * width

    def set_pixel(self, index, material):
        assert 0 <= index < self.width
        assert isinstance(material, MaterialComponent)
        self.buffer[index] = material.material

    def clear(self, material):
        assert isinstance(material, str) and len(material) == 1
        self.buffer[:] = [material] * self.width

    def output(self):
        return "".join(self.buffer)


class Display(object):
    PERMITTED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()`~-_=+[]{}\\|'\";:,.<>/? ")

    def __init__(self, width):
        assert width >= 0
        self.width = width

    def __enter__(self):
        return self

    def submit_frame(self, framebuffer):
        assert framebuffer.width == self.width
        output = framebuffer.output()
        assert set(output) <= self.PERMITTED_CHARS
        print(output, end="\r")
        sys.stdout.flush()

    def __exit__(self, *_):
        print()

from typing import Optional, cast

from .hardware import Framebuffer
from viperscene.components import TransformComponent, MaterialComponent
from viperscene.ecs import Scene
from viperscene.graphics.hardware import Display


class Renderer(object):
    def __init__(self, display: "Display", scene: Scene) -> None:
        self.display = display
        self.framebuffer = Framebuffer(display.width)
        self.rasterizer = Rasterizer(self.framebuffer, scene.background)
        self.scene = scene

    def render(self) -> None:
        self.rasterizer.draw_background()

        for entity in self.scene.registry:
            transform = cast(
                Optional[TransformComponent], entity.get_component(TransformComponent)
            )
            material = cast(
                Optional[MaterialComponent], entity.get_component(MaterialComponent)
            )

            if transform and material:
                self.rasterizer.draw_point(int(transform.pos_x + 0.5), material)

        self.display.submit_frame(self.framebuffer)


class Rasterizer(object):
    def __init__(self, framebuffer: Framebuffer, background: MaterialComponent) -> None:
        self.framebuffer = framebuffer
        self.background = background

    def draw_background(self) -> None:
        self.framebuffer.clear(self.background)

    def draw_point(self, pos: int, material: MaterialComponent) -> None:
        # Visibility test
        if 0 <= pos < self.framebuffer.width:
            self.framebuffer.set_pixel(pos, material)

    def draw_line(self, start: int, end: int, material: MaterialComponent) -> None:
        # Inclusive of both endpoints
        # Swap if needed
        if end > start:
            start, end = end, start

        # Visibility test
        if end >= 0 and start < self.framebuffer.width:
            for index in range(start, end + 1):
                self.framebuffer.set_pixel(index, material)

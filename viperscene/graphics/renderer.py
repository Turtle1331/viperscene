from .hardware import Framebuffer
from viperscene.components import TransformComponent, MaterialComponent


class Renderer(object):
    def __init__(self, display, scene):
        self.display = display
        self.framebuffer = Framebuffer(display.width)
        self.rasterizer = Rasterizer(self.framebuffer, scene.background)
        self.scene = scene
    
    def render(self):
        self.rasterizer.draw_background()

        for entity in self.scene.registry:
            transform = entity.get_component(TransformComponent)
            material = entity.get_component(MaterialComponent)

            if transform and material:
                self.rasterizer.draw_point(int(transform.pos_x + 0.5), material)

        self.display.submit_frame(self.framebuffer)


class Rasterizer(object):
    def __init__(self, framebuffer, background):
        self.framebuffer = framebuffer
        self.background = background

    def draw_background(self):
        self.framebuffer.clear(self.background)

    def draw_point(self, pos, material):
        # Visibility test
        if 0 <= pos < self.framebuffer.width:
            self.framebuffer.set_pixel(pos, material)

    def draw_line(self, start, end, material):
        # Inclusive of both endpoints
        # Swap if needed
        if end > start:
            start, end = end, start
        
        # Visibility test
        if end >= 0 and start < self.framebuffer.width:
            for index in range(start, end + 1):
                self.framebuffer.set_pixel(index, material)



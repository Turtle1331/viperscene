#!/usr/bin/env python3

import context
from viperscene import *

import time


def main():
    scene = Scene(".")

    scene.add_entity(
        Entity()
        .add_component(TransformComponent, 4)
        .add_component(MaterialComponent, "O")
        .add_component(ScriptComponent, "bounce.wat", {
            TransformComponent: (["pos_x"], True),
        })
    )

    with Display(16) as display:
        renderer = Renderer(display, scene)
        try:
            dt = 0.25
            while True:
                scene.update(dt)
                renderer.render()
                time.sleep(dt)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()


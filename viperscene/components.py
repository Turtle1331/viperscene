from typing import Any

from viperscene.ecs import Component


class TransformComponent(Component):
    def __init__(self, _: Any, pos_x: float = 0.0) -> None:
        self.pos_x = float(pos_x)


class MaterialComponent(Component):
    def __init__(self, _: Any, material: str) -> None:
        if len(material) != 1:
            raise ValueError(
                f"Expected material string with length one, got {material!r}"
            )
        self.material = str(material)

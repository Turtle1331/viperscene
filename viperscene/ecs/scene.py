from typing import Set, Iterator, Optional, cast, Union

from viperscene.scripting import ScriptComponent
from viperscene.components import MaterialComponent
from viperscene.ecs import Entity


class Registry:
    def __init__(self) -> None:
        self.entities: Set[Entity] = set()

    def __iter__(self) -> Iterator[Entity]:
        return iter(self.entities.copy())

    def add_entity(self, entity: Entity) -> None:
        self.entities.add(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)


class Scene:
    def __init__(self, background: Union[MaterialComponent, str] = " ") -> None:
        if isinstance(background, str):
            background = MaterialComponent(None, background)
        self.background = background
        self.registry = Registry()

    def add_entity(self, entity: Entity) -> None:
        self.registry.add_entity(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.registry.remove_entity(entity)

    def update(self, dt: float) -> None:
        for entity in self.registry:
            script = cast(
                Optional[ScriptComponent], entity.get_component(ScriptComponent)
            )
            if script:
                script.update(dt)

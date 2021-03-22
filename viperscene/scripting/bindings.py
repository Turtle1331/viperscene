from typing import Dict, List, Tuple, Type

from viperscene.ecs import Entity, Component
from .script import ScriptAsset, ScriptEnvironment, ScriptInstance


class ScriptComponent(Component):
    def __init__(self, entity: Entity, path: str, bindings: Dict[Type[Component], Tuple[List[str], bool]]) -> None:
        self.path = path
        self.asset = ScriptAsset(path)
        self.env = ScriptEnvironment(self.asset)
        self.instance = ScriptInstance(self.env)

        assert isinstance(entity, Entity)
        self.entity = entity
        self.bindings = bindings.copy()

    def on_added(self) -> None:
        self.instance.setup()

    def update(self, dt: float) -> None:
        for comp_type, binding in self.bindings.items():
            attrs: List[str]
            writable: bool
            attrs, writable = binding
            if writable:
                component = self.entity.get_component(comp_type)
                self.instance.set_component_values({attr: getattr(component, attr) for attr in attrs})

        self.instance.update(dt)
        values = self.instance.get_component_values()

        for comp_type, binding in self.bindings.items():
            attrs, writable = binding
            if writable:
                self.entity.update_component(comp_type, *(values.get(attr) for attr in attrs))

from .script import ScriptAsset, ScriptEnvironment, ScriptInstance
from viperscene.ecs import Entity, Component


class ScriptComponent(Component):
    def __init__(self, entity, path, bindings):
        self.path = path
        self.asset = ScriptAsset(path)
        self.env = ScriptEnvironment(self.asset)
        self.instance = ScriptInstance(self.env)

        assert isinstance(entity, Entity)
        self.entity = entity
        self.bindings = bindings.copy()

    def on_added(self):
        self.instance.setup()

    def update(self, dt):
        for comp_type, binding in self.bindings.items():
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

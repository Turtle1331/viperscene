from .component import Component

class Entity(object):
    def __init__(self):
        self.components = {}

    def get_component(self, comp_type):
        assert issubclass(comp_type, Component)
        return self.components.get(comp_type)

    def add_component(self, comp_type, *args, **kwargs):
        assert issubclass(comp_type, Component)
        assert comp_type not in self.components
        self.components[comp_type] = comp_type(self, *args, **kwargs)
        self.components[comp_type].on_added()
        return self

    def remove_component(self, comp_type):
        assert issubclass(comp_type, Component)
        assert comp_type in self.components
        self.components.pop(comp_type).on_removed()
        return self

    def update_component(self, comp_type, *args, **kwargs):
        self.remove_component(comp_type)
        self.add_component(comp_type, *args, **kwargs)

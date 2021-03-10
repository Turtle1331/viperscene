from viperscene.scripting import ScriptComponent

class Registry(object):
    def __init__(self):
        self.entities = set()

    def __iter__(self):
        return iter(self.entities.copy())

    def add_entity(self, entity):
        self.entities.add(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)


class Scene(object):
    def __init__(self, background=" "):
        self.background = background
        self.registry = Registry()

    def add_entity(self, entity):
        self.registry.add_entity(entity)

    def remove_entity(self, entity):
        self.registry.remove_entity(entity)

    def update(self, dt):
        for entity in self.registry:
            script = entity.get_component(ScriptComponent)
            if script:
                script.update(dt)




from viperscene.ecs import Component

class TransformComponent(Component):
    def __init__(self, _, pos_x=0.0):
        self.pos_x = float(pos_x)

class MaterialComponent(Component):
    def __init__(self, _, material):
        assert isinstance(material, str) and len(material) == 1
        self.material = str(material)

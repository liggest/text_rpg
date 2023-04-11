
from itertools import chain

from text_rpg.component import Component, Components, Status

class Entity:
    """  实体，游戏中实际存在的东西  """
    
    name = ""
    description = ""
    default_components:list[type[Component]] = None

    _components: Components | None = None

    @property
    def components(self):
        if not self._components:
            self._components = Components()
        return self._components

    def __init__(self, name=""):
        self.name = name

        if self.default_components:
            for c in self.default_components:
                self.components.add(c(self))  # 组件初始化

    def update(self):        
        if self._components:
            for c in chain(*self.components.values()):
                c.update(self)


class Creature(Entity):
    """  生物  """

    default_components = ( Status,  )

class World(Entity):
    """  世界  """

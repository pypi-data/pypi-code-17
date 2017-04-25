"""A simple, lightweight Entity Component System framework."""

from uuid import uuid4

class ECS(object):
    """A base ECS container object for containing and binding entities, components and systems together.

    Attributes:
        `entities` (list): list of all entities in the current ECS.
        `components` (dict): a dict of component-names. Value are a list of all components of that class.
        `systems` (list): a list of all systems in the current ECS.
    """
    def __init__(self):
        self.entities = []
        self.systems = []
        self.components = {}

    def AddEntity(self):
        """Adds a new entity to the current ECS.

        Returns:
            `entity` (ecs.Entity)
        """
        entity = Entity(self)
        self.entities.append(entity)
        return entity

    def DeleteEntity(self, entity):
        """Removes the referenced entity from the entities list.

        Arguments:
            `entity` (ecs.Entity): the entity to be removed.
        """
        self.entities.remove(entity)

    def AddSystem(self, system):
        """Adds the system to the systems list.

        Arguments:
            `system` (ecs.System): a system object to add to the ECS.

        Returns:
            `system` (ecs.System)
        """
        self.systems.append(system)
        return system

    def DeleteSystem(self, system):
        """Removes the referenced system from the systems list.

        Arguments:
            `system` (ecs.System): the system to be removed.
        """
        self.systems.remove(system)



class Entity(object):
    """An entity. Nothing more than an ID and 0+ components.

    Attributes:
        `uuid` (uuid4): the identifying UUID for the entity.
        `components` (dict): a dict of unique components, with the component class name as key and the component object as value.
        `ecs` (ecs.ECS): a reference to the parent ECS.
    """
    def __init__(self, ecs):
        self.uuid = uuid4()
        self.components = {}
        self.ecs = ecs

    def __repr__(self):
        return str(self.uuid)

    def Delete(self):
        """Removes this entity from the entities list of the parent ECS."""
        self.ecs.DeleteEntity(self)

    def AddComponent(self, component):
        """Adds a component to this entity.

        Arguments:
            `component` (ecs.Component): a component-object to add to the entity.
        """
        if not self.GetComponentByName(str(component)) and not component.parent_entity:
            self.components[str(component)] = component
            component.parent_entity = self

            if not str(component) in self.ecs.components:
                self.ecs.components[str(component)] = []
            self.ecs.components[str(component)].append(component)

    def RemoveComponent(self, component_name):
        """Removes a component by it's class name.

        Arguments:
            `component_name` (string): the class name of the component to remove.
        """
        self.components.pop(component_name)

    def GetComponentByName(self, component_name):
        """Looks for a component by its class name.

        Arguments:
            `component_name` (string): the class name of the component to retrieve.

        Returns:
            `component` (ecs.Component)
        """
        for component in self.components:
            if str(component) == component_name:
                return component


class Component(object):
    """A base-class of a component for an entity.

    Note:
        Remember to call `super().__init__()` when subclassing.

    Attributes:
        `parent_entity` (ecs.Entity): the parent entity of this component.
    """
    def __init__(self):
        self.parent_entity = None

    def __str__(self):
        return self.__class__.__name__


class System(object):
    """A base-class of a system to handle components.

    Note:
        Remember to call `super().__init__()` when subclassing.
        Subclasses should implement Execute()

    Attributes:
        `ecs` (ecs.ECS): a reference to the parent ECS.
        `component_class` (string): the class-name of the component this system handles.
    """
    def __init__(self, ecs, component_class=None):
        self.ecs = ecs
        self.component_class = component_class

    def __str__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.component_class)

    def Components(self):
        """Returns a list of all components of the system `component_class`."""
        return self.ecs.components[self.component_class]

    def Execute(self):
        """Common method for executing the system code.

        Note:
            This method must be implemented in a subclass.
        """
        raise NotImplementedError

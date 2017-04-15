import sys
import pytmx
from actors import *
from gamecontrollermt.predefined_classes import *
from pytmx.util_pygame import load_pygame


class TiledMap:
    def __init__(self, filename, world, gw, gh):
        tm = load_pygame(filename, pixelalpha=True)
        self.world = world

        self.walls = self.world.walls
        self.itemList = self.world.itemList
        self.actorList = self.world.actorList
        self.userIns = self.world.userInstance
        self.playerList = self.world.playerList

        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

        self.worldWidthZero = (gw - self.width)/2
        self.worldHeightZero = (gh - self.height)/2

    def _render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def _make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self._render(temp_surface)
        return temp_surface

    def _fill_map(self):
        for tile_object in self.tmxdata.objects:
            object_props = tile_object.properties
            self._object_factory(tile_object.name,
                               tile_object.x + self.worldWidthZero,
                               tile_object.y + self.worldHeightZero,
                               tile_object.width, tile_object.height,
                               object_props)

    def _object_factory(self, objName, x, y, width=0, height=0, object_properties=[]):
        actor = getattr(sys.modules[__name__], objName)
        subclasses = Actor.__subclasses__()
        superclasses = actor.__mro__

        if(actor in subclasses):
            if(Item in superclasses):
                name = 'Item' + str(len(self.itemList)) + '_' + objName
                actor = actor(x, y, name)
                for prop in object_properties:
                    if (hasattr(actor, prop)):
                        setattr(actor, prop, self._set_type(object_properties[prop]))
                actor.set_group(self.itemList)

            elif(IActor in superclasses):
                name = objName + str(len(self.actorList))
                actor = actor(x, y, name)
                for prop in object_properties:
                    if (hasattr(actor, prop)):
                        setattr(actor, prop, self._set_type(object_properties[prop]))
                actor.set_group(self.actorList)

            elif (Player in superclasses):
                name = objName + str(len(self.playerList))
                actor = actor(x, y, name)
                for prop in object_properties:
                    if (hasattr(actor, prop)):
                        setattr(actor, prop, self._set_type(object_properties[prop]))
                actor.set_group(self.playerList)
                self.world.player = actor

            else:
                name = 'UI' + str(len(self.userIns)) + '_' + objName
                actor = actor(x, y, name)
                for prop in object_properties:
                    if (hasattr(actor, prop)):
                        setattr(actor, prop, self._set_type(object_properties[prop]))
                actor.set_group(self.userIns)

            actor.set_world(self.world)

        elif(actor.__name__ == 'Wall'):
            Wall(self.world, x, y, width, height, self.walls)

    def _set_type(self, atr):
        try:
            atr = float(atr)
            return atr
        except ValueError as e:
            if (atr in ['True', 'False']):
                return bool(atr)
            else:
                return atr

    def add_actor_to_map(self, objName, x, y, width=0, height=0, object_properties=[]):
        self._object_factory(objName, x, y, width, height, object_properties)

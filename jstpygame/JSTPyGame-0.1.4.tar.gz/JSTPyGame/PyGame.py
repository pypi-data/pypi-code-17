#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Scenes import *


class Engine(object):
    """This class is the game engine."""

    def __init__(self, scene_map, player):
        self.scene_map = scene_map
        self.player = player
        # To define the keyboard entry to bypass the scene
        self.cheatcode = "p"
        print texts.get(type(self).__name__)

    def play(self):
        """This method manages the progress in the map"""

        current_scene = self.scene_map.opening_scene
        # run current_scene.enter() and return teh next_scene to run
        while True:
            # Defin the number of parameters to give for "enter" method
            if isinstance(current_scene, Death) or isinstance(current_scene, Victory) \
                                                or isinstance(current_scene, EmptyRoom):
                current_scene = current_scene.enter()
            elif isinstance(current_scene, Cell):
                current_scene = current_scene.enter(self.scene_map, self.player)
            else:
                current_scene = current_scene.enter(self.scene_map, self.player, self.cheatcode)


def start():
    a_player = Player()
    a_map = Map()
    a_engine = Engine(a_map, a_player)
    a_engine.play()


start()

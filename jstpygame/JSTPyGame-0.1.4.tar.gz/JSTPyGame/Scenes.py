#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Texts import texts
from Characters import *
from termcolor import colored
from random import shuffle


class Death(object):
    """Class for death scene"""

    def enter(self):
        print '_'*40
        print colored(texts.get(type(self).__name__), 'red')
        exit(0)


class Victory(object):
    """Class called when you win"""

    def enter(self):
        print '_'*40
        print texts.get(type(self).__name__)
        exit(0)


class DungeonGate(object):
    """Class for start scene.
        The player must pass the heavy guard to enter in the dungeon"""

    def enter(self, map_instance, player_instance, cheatcode):
        print '_'*40
        print texts.get(type(self).__name__)
        action = raw_input("Réponse> ")
        if action == "lancer du gravier sur le cheval" or action == "lancer un caillou sur le cheval"\
                     or action == cheatcode:
            print texts.get("DungeonGate_cheval")
            return Corridor()
        elif action == "attaquer le garde":
            a_guard = HeavyGuard()
            fight_result = player_instance.fight(a_guard.name, a_guard.characteristics, cheatcode)
            if fight_result == 'alive':
                player_instance.print_charac()
                print texts.get("DungeonGate_combat")
                map_instance.explored_scenes['DungeonGate'] = "explored"
                return Corridor()
            else:
                return Death()
        else:
            print colored("Je ne comprends pas votre ordre. retour en début de scéne.", 'red')
            return DungeonGate()


class Corridor(object):
    """Class for Corridor room."""

    def enter(self, map_instance, player_instance, cheatcode):

        # if the player has released is wife when in open in the Corridor
        if map_instance.explored_scenes['Cell'] == "explored":
            enemies = []

            # Define the number of enemies in the corridor
            if map_instance.explored_scenes['DungeonGate'] == "explored":
                pass
            else:
                a_heavyguard = HeavyGuard()
                enemies.append(a_heavyguard)

            if map_instance.explored_scenes['Dormitory'] == "explored":
                pass
            else:
                a_guard = Guard()
                enemies.append(a_guard)

            if not enemies:
                return Victory()
            else:
                print '_'*40
                print texts.get("Corridor_fight").format(len(enemies))

                for enemi in enemies:
                    fight_result = player_instance.fight(enemi.name, enemi.characteristics, cheatcode)

                    if fight_result == 'alive':
                        pass
                    else:
                        return Death()

                player_instance.print_charac()
                return Victory()

        else:
            print '_'*40
            print texts.get(type(self).__name__)
            answer = raw_input("Réponse> ")

            if answer == cheatcode:
                print colored("ORDRE DES SALLES:", attrs=['bold'])
                i = 1

                for scene in map_instance.corridor_scenes:
                    print i, "-", type(scene).__name__
                    i += 1

                return Corridor()
            next_scene = map_instance.corridor_scenes[int(answer)-1]

            # check if the selected scene is already explored or not
            if map_instance.explored_scenes[type(next_scene).__name__] == "unexplored":
                return next_scene
            elif map_instance.explored_scenes[type(next_scene).__name__] == "explored":
                print colored("Salle déja explorée", 'magenta')
                return Corridor()
            else:
                print colored("Je ne comprends pas votre ordre. retour en début de scéne.", 'red')
                return Corridor()


class GuardsRoom(object):
    """Class for guards's room.
    The key required to release the player's wife is in this room with 2 guards"""

    def enter(self, map_instance, player_instance, cheatcode):
        print '_'*40
        print texts.get("GuardsRoom_intro")

        for i in range(2):
            a_guard = Guard()
            fight_result = player_instance.fight(a_guard.name, a_guard.characteristics, cheatcode)

            if fight_result == 'alive':
                pass
            else:
                return Death()

        map_instance.explored_scenes[type(self).__name__] = "explored"
        player_instance.key = 'yes'
        player_instance.print_charac()
        print texts.get("GuardsRoom_outro")
        return Corridor()


class Cell(object):
    """Class for cell room.
    You must have the cell's key to release your wife."""

    def enter(self, map_instance, player_instance):
        print '_'*40
        print texts.get("Cell_intro")

        if player_instance.key == 'yes':
            print texts.get("Cell_with_key")
            map_instance.explored_scenes['Cell'] = "explored"
        else:
            print texts.get("Cell_without_key")

        return Corridor()


class Dormitory(object):
    """Class for dormitory.
    a guard sleep in this room.
    after fighting the guard, you gain an armor"""

    def enter(self, map_instance, player_instance, cheatcode):
        print '_'*40
        print texts.get(type(self).__name__)
        a_guard = Guard()
        fight_result = player_instance.fight(a_guard.name, a_guard.characteristics, cheatcode)

        if fight_result == 'alive':
            print texts.get("Dormitory_armor")
            player_instance.characteristics['armor'] += 2
            player_instance.print_charac()
            map_instance.explored_scenes[type(self).__name__] = "explored"
            return Corridor()
        else:
            return Death()


class Armory(object):
    """Class for armory.
    This locked room by a code contains a sword"""

    def enter(self, map_instance, player_instance, cheatcode):
        print '_'*40
        print texts.get(type(self).__name__)
        answer = raw_input('Réponse? ')
        if answer == '1':
            enemies = []
            # Define the number of enemies in the room
            if map_instance.explored_scenes['GuardsRoom'] == "explored":
                pass
            else:
                for i in range(2):
                    a_guard = Guard()
                    enemies.append(a_guard)

            if map_instance.explored_scenes['Dormitory'] == "explored":
                pass
            else:
                a_guard = Guard()
                enemies.append(a_guard)

            if not enemies:
                print texts.get('Armory_weapon')
                player_instance.characteristics['weapon'] += 2
                player_instance.print_charac()
                map_instance.explored_scenes['Armory'] = "explored"
                return Corridor()
            else:
                print '_'*40
                print texts.get("Armory_fight").format(len(enemies))
                for enemi in enemies:
                    fight_result = player_instance.fight(enemi.name, enemi.characteristics, cheatcode)

                    if fight_result == 'alive':
                        pass
                    else:
                        return Death()

                player_instance.characteristics['weapon'] += 2
                player_instance.print_charac()
                map_instance.explored_scenes['Armory'] = "explored"
                return Corridor()

        elif answer == '2':
            attempts = 0
            code = "{}{}{}".format(randint(0, 9), randint(0, 9), randint(0, 9))
            while attempts < 10:
                answer = raw_input("Code? ")

                if answer == code or answer == cheatcode:
                    print texts.get('Armory_weapon')
                    player_instance.characteristics['weapon'] += 2
                    map_instance.explored_scenes['Armory'] = "explored"
                    player_instance.print_charac()
                    return Corridor()

                else:
                    attempts += 1
                    hint = ['*', '*', '*']
                    for character in answer:
                        for i in range(len(code)):
                            if character == code[i]:
                                hint[i] = character
                    print "Hint:", "".join(map(str, hint))

            print "vous avez fait trop de tentatives. Revenez plus tard."
            return Corridor()

        elif answer == '3':
            return Corridor()
        else:
            print colored("Je ne comprends pas votre ordre. retour en début de scéne.", 'red')
            return Armory()


class EmptyRoom(object):
    """Class for empry rooms linked to corridor."""

    def enter(self):
        print texts.get(type(self).__name__)
        return Corridor()


class Map(object):
    """This class defines the sequence between scenes and the start scene."""
    # This dict define the next scene from a scene.

    def __init__(self):
        """Where you define the start scene"""
        self.opening_scene = DungeonGate()
        # this list define the order of scenes in the corridor
        self.corridor_scenes = [GuardsRoom(), Cell(), Armory(), EmptyRoom(), Dormitory()]
        shuffle(self.corridor_scenes)
        self.explored_scenes = {
                                "GuardsRoom": "unexplored",
                                "Cell": "unexplored",
                                "Dormitory": "unexplored",
                                "Armory": "unexplored",
                                "EmptyRoom": "unexplored",
                                "DungeonGate": "unexplored"
                                }

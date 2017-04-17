# -*- coding: utf-8 -*-
from random import randint
from termcolor import colored


class Human(object):
    """Base class for all characters in the game."""

    def __init__(self, life):
        self.characteristics = {
                                'life': life,
                                'weapon': 0,
                                'armor': 0
                                }


class Player(Human):
    """Class for the player."""

    def __init__(self):
        super(Player, self).__init__(randint(10, 15))
        self.key = 'no'
        print '_'*40
        self.print_charac()

    def print_charac(self):
        """Method to print the player characteristics"""

        print colored("Votre héros a les caractéristiques suivantes:\n\t- {} points de vie\n\t- {} bonus d'attaque"
                      "\n\t- {} point d'armure".format(self.characteristics['life'],
                                                       self.characteristics['weapon'],
                                                       self.characteristics['armor']),
                      'blue')

    def fight(self, opponent_name, opponent_characteristics, cheatcode):
        """Method called to manage fights between player and opponents"""

        self.print_charac()
        print colored("L'énnemi est un {} et a les caractéristiques suivantes:\n\t- {} points de vie"
                      "\n\t- {} bonus d'attaque\n\t- {} point d'armure".format(opponent_name,
                                                                               opponent_characteristics['life'],
                                                                               opponent_characteristics['weapon'],
                                                                               opponent_characteristics['armor']),
                      'magenta')
        wait = raw_input("Press enter to continue.")

        # gestion du cheatcode
        if wait == cheatcode:
            return 'alive'

        print colored("LE COMBAT:", attrs=['bold'])

        while self.characteristics['life'] > 0:
            attack = randint(1, 6) + self.characteristics['weapon']
            print colored("Vous avez effectué une attaque de {}".format(attack), 'blue')
            # check if opponent dodge the attack or not
            dodge = randint(1, 10)

            if opponent_characteristics['armor'] > 0:
                if self.characteristics['armor'] > 0:
                    value = 7
                else:
                    value = 10
            else:
                if self.characteristics['armor'] > 0:
                    value = 6
                else:
                    value = 9

            if dodge < value:
                if attack > opponent_characteristics['armor']:
                    opponent_characteristics['life'] -= (attack - opponent_characteristics['armor'])
            else:
                print colored("Le {} a paré l'attaque.".format(opponent_name), 'magenta')

            if opponent_characteristics['life'] > 0:
                print colored("\tIl reste {} points de vie à votre adversaire".format(opponent_characteristics['life']),
                              'magenta')
                enemi_attack = randint(1, 6) + opponent_characteristics['weapon']
                print colored("Le {} effectue une attaque de {}".format(opponent_name, enemi_attack), 'magenta')
                # check if you dodge the attack or not
                dodge = randint(1, 10)

                if opponent_characteristics['armor'] > 0:
                    if self.characteristics['armor'] > 0:
                        value = 5
                    else:
                        value = 3
                else:
                    if self.characteristics['armor'] > 0:
                        value = 7
                    else:
                        value = 5

                if dodge < value:
                    self.characteristics['life'] -= (enemi_attack - self.characteristics['armor'])

                    if self.characteristics['life'] > 0:
                        print colored("\tIl vous reste {} points de vie".format(self.characteristics['life']), 'blue')
                    else:
                        print colored("\tVous êtes mort", 'red')
                        return 'dead'
                else:
                    print colored("Vous avez paré l'attaque.", 'blue')
            else:
                print colored("Vous avez vaincu le garde", 'green')
                return 'alive'


class Guard(Human):
    """class for enemies in the game."""

    name = "garde léger"

    def __init__(self):
        super(Guard, self).__init__(10)
        self.name = "garde léger"


class HeavyGuard(Guard):
    """subclass of Guard for more powerfull enemies"""

    name = "garde lourd"

    def __init__(self):
        self.characteristics = {
                                'life': 10,
                                'weapon': 2,
                                'armor': 2
                                }

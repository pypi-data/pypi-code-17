# ~*~ coding: utf-8 ~*~

# (C) 2017, Eike Jesinghaus
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

from .collectibles import Spasmolytic
from .levels import LevelStart

class Dungeon(object):
    def __init__(self, theme, room_count, keylevel_increment_counter=5):
        self.theme = theme
        self.room_count = room_count
        self.rooms = []
        self.keylevel_increment_counter = keylevel_increment_counter

        for i in range(0, 11):
            self.rooms.append([None, None, None, None, None, None, None, None, None, None, None])

    def generate(self, levels, bosslevels):
        count = 0
        keylevel = 0

        self.rooms[5][5] = LevelStart(self.theme, keylevel)
        self.rooms[5][5].label = "S"

        while count < self.room_count:

            parentroom = None
            while parentroom is None:
                y = random.randint(0, 10)
                x = random.randint(0, 10)
                parentroom = self.rooms[y][x]

            if parentroom.keylevel != keylevel:
                continue

            adjacent = [(x, y-1, "up", "down"), (x, y+1, "down", "up"), (x-1, y, "left", "right"), (x+1, y, "right", "left")]
            for i in adjacent:
                if -1 in i or 11 in i:
                    adjacent.remove(i)

            adjacent_empty = []
            for i in adjacent:
                if self.rooms[i[1]][i[0]] is None:
                    adjacent_empty.append(i)

            if len(adjacent_empty) == 0:
                continue

            if (count > 0 and count % self.keylevel_increment_counter == 0) or count == self.room_count - 1:
                keylevel += 1

            coords = random.choice(adjacent_empty)
            level_group = levels
            if count == self.room_count - 1:
                level_group = bosslevels
            self.rooms[coords[1]][coords[0]] = random.choice(level_group)(self.theme, keylevel)
            childroom = self.rooms[coords[1]][coords[0]]

            setattr(parentroom, coords[2], (childroom, (childroom.keylevel > parentroom.keylevel)))
            setattr(childroom, coords[3], (parentroom, False))

            parentroom.children.append(childroom)
            childroom.parent = parentroom

            count = 0
            for i in self.rooms:
                for j in i:
                    if j is not None:
                        count += 1

        childroom.label = "B"

        keys = 0
        while keys < keylevel:

            room = None
            while room is None:
                y = random.randint(0, 10)
                x = random.randint(0, 10)
                room = self.rooms[y][x]

            if room.keylevel != keys or room.label in "SB":
                continue

            room.contains = Spasmolytic(room.keypos)
            room.label = "K"
            keys += 1

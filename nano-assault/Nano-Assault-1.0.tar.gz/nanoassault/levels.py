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

from .collectibles import Energy
from .enemies import CoccusDesertus, CoccusIactans, CoccusImmanis, BacillusCeler
from .level import Level

class LevelStart(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), (), keylevel)

class LevelCDCorner(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((CoccusDesertus, (2, 2)), (CoccusDesertus, (13, 2)), (CoccusDesertus, (2, 9)), (CoccusDesertus, (13, 9))), keylevel)

class LevelCIMid(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((CoccusIactans, (7.5, 5.5)),), keylevel)

class LevelCITwo(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((CoccusIactans, (6, 5)), (CoccusIactans, (9, 5))), keylevel)

class LevelCICD(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((CoccusDesertus, (4, 4)), (CoccusDesertus, (11, 4)), (CoccusDesertus, (4, 7)), (CoccusDesertus, (11, 7)), (CoccusIactans, (7.5, 5.5))), keylevel, Energy((7.5, 5.5)))

class LevelBossCI(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((CoccusImmanis, (7, 5)),), keylevel)

class LevelBC(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((BacillusCeler, (7, 5)),), keylevel)

class LevelBCCD(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((BacillusCeler, (7, 5)), (CoccusDesertus, (8, 5))), keylevel)

class LevelBCThree(Level):
    def __init__(self, theme, keylevel):
        Level.__init__(self, theme, (), ((BacillusCeler, (5, 5)), (BacillusCeler, (7, 5)), (BacillusCeler, (9, 5))), keylevel)

ALL_LEVELS = []
BOSS_LEVELS = []
for i in Level.__subclasses__():
    if i.__name__.startswith("LevelBoss"):
        BOSS_LEVELS.append(i)
    else:
        ALL_LEVELS.append(i)

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

from .animation import Animation

anim_player_walking = Animation(("player_walking0", "player_walking1", "player_walking2", "player_walking3", "player_walking2", "player_walking1"), 10)
animations_player = (anim_player_walking,)

def animations_enemy_coccusdesertus(): return (Animation(("enemy_coccusdesertus_walking0", "enemy_coccusdesertus_walking1"), 6),
                                               Animation(("enemy_coccusdesertus_walking0",), 0),)
def animations_enemy_coccusiactans(): return (Animation(("enemy_coccusiactans_walking0",), 0),
                                              Animation(("enemy_coccusiactans_standing0",), 0),)
def animations_boss_coccusimmanis(): return (Animation(("boss_coccusimmanis_walking0",), 0),
                                             Animation(("boss_coccusimmanis_walking1",), 0),)
def animations_enemy_bacillusceler(): return (Animation(("enemy_bacillusceler_walking0",), 0),
                                             Animation(("enemy_bacillusceler_walking1",), 0),)

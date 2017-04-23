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

import os

from .bullets import BulletPlayer
from .collectibles import Energy
from .constants import SCALEFAC, FPS, TILEX, TILEY

import pygame


pygame.init()

def quit_():
    exit(0)

def gameover():
    quit_()

def run_level(screen, level, player):

    ui_heart = pygame.image.load(os.path.join(os.path.dirname(__file__), "img", "ui_heart.png"))
    ui_heart = pygame.transform.scale(ui_heart, (ui_heart.get_width()*SCALEFAC, ui_heart.get_height()*SCALEFAC))

    sound_pickup = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sound", "pickup.wav"))
    sound_open = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sound", "open.wav"))
    sound_hit = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sound", "hit0.wav"))

    clock = pygame.time.Clock()

    bg = level.generate_bg()

    collectibles = pygame.sprite.RenderClear()
    doors = pygame.sprite.RenderClear()
    players = pygame.sprite.RenderClear()
    bullets = pygame.sprite.RenderClear()
    enemies = pygame.sprite.RenderClear()
    walls = pygame.sprite.RenderClear()

    players.add(player)

    walls.add(*level.generate_walls())
    walls.draw(bg)

    enemies.add(*level.generate_enemies())
    doors.add(*level.generate_doors())

    screen.blit(bg, (0, 0))

    doors.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_()
                elif event.key == pygame.K_w:
                    player.motion[1] = -1
                elif event.key == pygame.K_s:
                    player.motion[1] = 1
                elif event.key == pygame.K_a:
                    player.motion[0] = -1
                elif event.key == pygame.K_d:
                    player.motion[0] = 1
                elif event.key == pygame.K_UP and not player.bullet_cooldown:
                    bullets.add(BulletPlayer(player.rect.center, (0, -1)))
                    player.bullet_cooldown = 30
                elif event.key == pygame.K_DOWN and not player.bullet_cooldown:
                    bullets.add(BulletPlayer(player.rect.center, (0, 1)))
                    player.bullet_cooldown = 30
                elif event.key == pygame.K_LEFT and not player.bullet_cooldown:
                    bullets.add(BulletPlayer(player.rect.center, (-1, 0)))
                    player.bullet_cooldown = 30
                elif event.key == pygame.K_RIGHT and not player.bullet_cooldown:
                    bullets.add(BulletPlayer(player.rect.center, (1, 0)))
                    player.bullet_cooldown = 30

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.motion[1] = 0
                    if pygame.key.get_pressed()[pygame.K_s]:
                        player.motion[1] = 1
                elif event.key == pygame.K_s:
                    player.motion[1] = 0
                    if pygame.key.get_pressed()[pygame.K_w]:
                        player.motion[1] = -1
                elif event.key == pygame.K_a:
                    player.motion[0] = 0
                    if pygame.key.get_pressed()[pygame.K_d]:
                        player.motion[0] = 1
                elif event.key == pygame.K_d:
                    player.motion[0] = 0
                    if pygame.key.get_pressed()[pygame.K_a]:
                        player.motion[0] = -1

        doors.clear(screen, bg)
        collectibles.clear(screen, bg)
        enemies.clear(screen, bg)
        players.clear(screen, bg)
        bullets.clear(screen, bg)

        if not player.update():
            gameover()

        for w in pygame.sprite.spritecollide(player, walls, False):
            player.coll_obstacle(w)

        for d in pygame.sprite.spritecollide(player, doors, False):
            player.coll_obstacle(d)
            if level.cleared and player.keys > 0:
                sound_open.play()
                player.keys -= 1
                d.kill()
                level.unlocked = True

        for c in pygame.sprite.spritecollide(player, collectibles, True):
            c.on_collect(player)
            sound_pickup.play()

        if player.rect.top < 16*SCALEFAC:
            player.rect.bottom = screen.get_height()-24*SCALEFAC
            return level.up[0]
        elif player.rect.left < 16*SCALEFAC:
            player.rect.right = screen.get_width()-16*SCALEFAC
            return level.left[0]
        elif player.rect.bottom > screen.get_height()-24*SCALEFAC:
            player.rect.top = 16*SCALEFAC
            return level.down[0]
        elif player.rect.right > screen.get_width()-16*SCALEFAC:
            player.rect.left = 16*SCALEFAC
            return level.right[0]

        enemies.update(player, bullets)

        if len(enemies) == 0 and len(collectibles) == 0:
            if not level.cleared:
                if len(level.enemies):
                    sound_open.play()
                level.clear(collectibles, doors)

        for e in pygame.sprite.spritecollide(player, enemies, False):
            sound_hit.play()
            e.contact(player)

        c = pygame.sprite.groupcollide(enemies, walls, False, False)
        for i in c:
            i.coll_obstacle(c[i])

        c = pygame.sprite.groupcollide(enemies, doors, False, False)
        for i in c:
            i.coll_obstacle(c[i])

        bullets.update()

        c = pygame.sprite.groupcollide(bullets, enemies, False, False)
        for i in c:
            if i.byplayer:
                sound_hit.play()
                i.hit(c[i][0])
                i.kill()

        for b in pygame.sprite.spritecollide(player, bullets, False):
            if not b.byplayer:
                b.hit(player)
                b.kill()

        doors.draw(screen)
        collectibles.draw(screen)
        enemies.draw(screen)
        players.draw(screen)
        bullets.draw(screen)

        pygame.draw.rect(screen, (10, 10, 10), (0, TILEY*16*SCALEFAC, TILEX*16*SCALEFAC, 8*SCALEFAC), 0)
        for i in range(0, player.hp+1):
            screen.blit(ui_heart, (i*SCALEFAC*8, TILEY*16*SCALEFAC))

        pygame.display.update()
        clock.tick_busy_loop(FPS)

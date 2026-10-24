"""Built-in castle traps.

Sprites: 'dart' (the trap block), 'dart_charge' (flash before firing), 'dart_shot' (the dart).
"""
import math

from settings import *
from sprites import Sprite
from spells import Projectile
import assets
import sounds


class DartTrap(Sprite):
    """A block (a Tiled object named 'DartTrap') that shoots a dart across the castle every few seconds.
    It flashes just before firing. It is solid, and the runner can block darts with the shield."""

    def __init__(self, pos, size, direction, offset, groups):
        super().__init__(pos, assets.get("dart", size), groups, Z_LAYERS['main'] + 0.1)
        self.dir = direction                  # +1 shoots right, -1 shoots left
        self.timer = offset
        self.t = 0.0                          # animation clock for the trap sprite
        self._swirl_ready = True

    @property
    def charging(self):
        return self.timer > DART_INTERVAL - DART_CHARGE

    def update(self, dt, level):
        self.t += dt
        self.timer += dt

        screen_rect = to_screen(self.rect, level.all_sprites.draw_offset)
        visible = screen_rect.colliderect(pygame.Rect(0, 0, WINDOW_WIDTH, VIEW_H))
        near = math.hypot(self.rect.centerx - level.runner.rect.centerx,
                          self.rect.centery - level.runner.rect.centery) <= 220

        if self.timer >= DART_INTERVAL:
            self.timer -= DART_INTERVAL
            w, h = DART_SIZE
            x = self.rect.right if self.dir > 0 else self.rect.left - w
            Projectile((x, self.rect.centery - h / 2), DART_SIZE, (self.dir * DART_SPEED, 0), "dart_shot",
                       (level.all_sprites, level.projectile_sprites))

            if visible and near:
                sounds.play("swirling")

        if not visible:
            self._swirl_ready = True
        elif near and self._swirl_ready:
            self._swirl_ready = False

    def draw(self, surface, offset):
        trap_rect = to_screen(self.rect, offset)
        assets.draw_block(surface, "dart", trap_rect, t=self.t)
        if self.charging:
            w, h = DART_SIZE
            x = self.rect.right - w if self.dir > 0 else self.rect.left
            flash = to_screen(pygame.FRect(x, self.rect.centery - h / 2, w, h), offset)
            if not assets.draw(surface, "dart_charge", flash, t=self.t, alpha=180):
                assets.draw_block(surface, "dart_shot", flash)
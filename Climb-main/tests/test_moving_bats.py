import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import pygame

from spells import MovingBat, FloodSpell, MossSpell
from level import Level


def test_bat_starts_where_clicked_inside_side_bounds():
    pygame.init()
    pygame.display.set_mode((1, 1))

    bat_left = MovingBat(70, 100, "left", (50, 200), ())
    assert bat_left.rect.x == 70
    assert bat_left.dir == 1

    bat_right = MovingBat(140, 100, "right", (50, 200), ())
    assert bat_right.rect.x == 140
    assert bat_right.dir == -1

    pygame.quit()


def test_solar_flare_is_unblockable_by_shield():
    class DummyRunner:
        def __init__(self):
            self.rect = pygame.FRect(90, 80, 20, 30)
            self.shield = 999
            self.hearts = 3
            self.hit_calls = 0

        @property
        def cx(self):
            return self.rect.centerx

        def hit(self, from_x):
            self.hit_calls += 1
            self.hearts -= 1

    level = Level.__new__(Level)
    level.runner = DummyRunner()
    level.height = 200
    level.solar_flare_active = True
    level.solar_flare_warn_t = 0.1
    level.solar_flare_hit_t = 0.0
    level.solar_flare_beam_x = 100

    level._update_solar_flare(0.2)

    assert level.runner.hit_calls == 2
    assert level.runner.hearts == 1


def test_flood_damages_once_then_dissappears():
    class DummyRunner:
        def __init__(self):
            self.rect = pygame.FRect(0, 0, 20, 20)
            self.hearts = 3
            self.hit_calls = 0

        @property
        def cx(self):
            return self.rect.centerx

        def hit(self, from_x):
            self.hit_calls += 1
            self.hearts -= 1

    level = Level.__new__(Level)
    level.runner = DummyRunner()
    level.typhoon_t = 0.0
    level.flood_active = True
    level.flood_t = 10.0
    level.flood_alarm_t = 0.0
    level.flood_y = 15.0

    level._update_flood(0.1)

    assert level.runner.hit_calls == 1
    assert level.flood_active is False
    assert level.flood_y == 0.0


def test_flood_spell_does_not_start_looping_flood_sound():
    calls = []

    class DummyRunner:
        def __init__(self):
            self.rect = pygame.FRect(100, 200, 20, 20)

    level = Level.__new__(Level)
    level.runner = DummyRunner()
    level.flood_active = False
    level.flood_t = 0.0
    level.flood_alarm_t = 0.0
    level.flood_y = 0.0

    import sounds
    original_play = sounds.play
    original_stop = sounds.stop
    try:
        def fake_play(name, loops=0):
            calls.append(("play", name, loops))
        def fake_stop(name):
            calls.append(("stop", name))
        sounds.play = fake_play
        sounds.stop = fake_stop
        FloodSpell().cast(level, (0, 0))
    finally:
        sounds.play = original_play
        sounds.stop = original_stop

    assert ("play", "flood", -1) not in calls
    assert level.flood_active is True


def test_moss_cast_during_typhoon_spawns_adjacent_moss():
    class Platform:
        def __init__(self, rect):
            self.rect = rect
            self.old_rect = rect.copy()

    class DummyRunner:
        def __init__(self):
            self.rect = pygame.FRect(0, 0, 16, 16)

    class DummyLevel:
        def __init__(self):
            self.typhoon_t = 1.0
            self.all_sprites = pygame.sprite.Group()
            self.moss_sprites = pygame.sprite.Group()
            self.runner = DummyRunner()
            self.semis = type('Semis', (), {
                'query': lambda self, rect: [Platform(pygame.FRect(0, 80, 64, 8))]
            })()
            self.solids = type('Solids', (), {'query': lambda self, rect: []})()

    level = DummyLevel()
    MossSpell().cast(level, (8, 72))

    assert len(level.moss_sprites) == 2
    xs = sorted(sprite.rect.x for sprite in level.moss_sprites.sprites())
    assert xs == [0, 16]

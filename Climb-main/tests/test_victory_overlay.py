import os
import sys

import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import game_scene


class DummyGame:
    def __init__(self):
        self.started = []

    def new_level(self):
        class DummyLevel:
            winner = "runner"
            countdown = 0.0
            progress = 1.0
            runner = type("Runner", (), {"inverted": 0})()
            typhoon_t = 0.0
            earthquake_t = 0.0
            solar_flare_active = False
            solar_flare_warn_t = 0.0
            flood_active = False
            flood_y = 0

        return DummyLevel()

    def start_match(self, roles):
        self.started.append(roles)

    def show_menu(self):
        self.started.append("menu")


def test_game_over_actions_are_short_side_by_side_links():
    pygame.init()
    game = DummyGame()
    scene = game_scene.GameScene(game, {"runner": "runner", "caster": "caster"})

    actions = scene._game_over_actions((0, 0))

    assert [action[0] for action in actions] == ["REMATCH", "MAIN MENU"]
    assert actions[0][1].right <= actions[1][1].left
    assert actions[0][2] == "rematch"
    assert actions[1][2] == "menu"

    assert scene._winner_text_color() == (255, 220, 60)

    pygame.quit()

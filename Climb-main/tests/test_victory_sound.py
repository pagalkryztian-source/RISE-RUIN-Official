import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import assets
import sounds
from game_scene import GameScene
from level import Level


def test_runner_animation_assets_resolve():
    for key in ["runner_idle", "runner_run", "runner_jump", "runner_hurt"]:
        assert assets.resolve(key) is not None
        assert assets.natural_size(key) is not None


def test_hud_uses_dedicated_runner_and_caster_panel_assets():
    assert "runner_panel" in assets.SPRITES
    assert "caster_panel" in assets.SPRITES
    assert assets.SPRITES["runner_panel"].get("fallback") == "hud_panel"
    assert assets.SPRITES["caster_panel"].get("fallback") == "hud_panel"


def test_level_set_winner_plays_victory_sound(monkeypatch):
    played = []
    monkeypatch.setattr(sounds, "play", lambda name, loops=0: played.append((name, loops)))

    level = Level.__new__(Level)
    level.winner = None

    level.set_winner("runner")
    assert level.winner == "runner"
    assert played == [("victory", 0)]

    level.set_winner("runner")
    assert played == [("victory", 0)]

    level.set_winner("caster")
    assert level.winner == "runner"
    assert played == [("victory", 0)]


def test_stop_all_sfx_keeps_victory_sound(monkeypatch):
    stopped = []
    fake_sfx = {
        "victory": type("SoundStub", (), {"stop": lambda self: stopped.append("victory")})(),
        "runner_jump": type("SoundStub", (), {"stop": lambda self: stopped.append("runner_jump")})(),
    }
    monkeypatch.setattr(sounds, "_sfx", fake_sfx)

    sounds.stop_all_sfx()

    assert stopped == ["runner_jump"]


def test_game_scene_accepts_menu_role_mapping():
    assert GameScene.resolve_players({"runner": "runner", "caster": "caster"}) == (1, 2)
    assert GameScene.resolve_players(["caster", "runner"]) == (1, 2)
    assert GameScene.resolve_players(["runner", "caster"]) == (2, 1)

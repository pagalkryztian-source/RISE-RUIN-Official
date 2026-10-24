import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import game
import menu


def test_menu_story_cycle_has_two_segments():
    assert hasattr(menu, "STORY_SEGMENTS")
    assert len(menu.STORY_SEGMENTS) == 2
    assert "We are all runners" in menu.STORY_SEGMENTS[0]
    assert "We are sometimes the Casters" in menu.STORY_SEGMENTS[1]


def test_map_selection_quotes_cycle_has_expected_entries():
    assert hasattr(menu, "MAP_SELECTION_QUOTES")
    assert len(menu.MAP_SELECTION_QUOTES) == 10
    assert "Every climb begins with a reason to keep going." in menu.MAP_SELECTION_QUOTES[0]
    assert "No storm lasts forever. Keep climbing." in menu.MAP_SELECTION_QUOTES[-1]


def test_show_map_selection_keeps_button_click_sound_enabled():
    g = game.Game.__new__(game.Game)

    with patch.object(game.sounds, "stop_all_sfx") as mock_stop, \
         patch.object(game, "MapSelectionScene") as mock_scene:
        g.show_map_selection()

    mock_stop.assert_not_called()
    assert mock_scene.called

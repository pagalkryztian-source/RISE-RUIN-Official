import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import menu


def test_menu_uses_custom_video_and_logo_assets():
    assert menu.MENU_ART["background_video"].endswith("Background_video_MainMenu.mp4")
    assert menu.MENU_ART["logo_path"].endswith("logo.png")
    assert os.path.isfile(menu.MENU_ART["background_video"])
    assert os.path.isfile(menu.MENU_ART["logo_path"])

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

import assets


def test_bounce_block_has_animation_frames():
    assert assets.resolve("bounce") is not None
    frames = assets._frames("bounce")
    assert frames is not None
    assert len(frames) >= 3


def test_earthquake_has_two_rock_animation_variants():
    assert assets.resolve("rock") is not None
    assert assets.resolve("rock_alt") is not None
    assert len(assets._frames("rock")) >= 3
    assert len(assets._frames("rock_alt")) >= 3

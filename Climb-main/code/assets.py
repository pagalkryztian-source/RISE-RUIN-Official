import math
import os

import pygame

from settings import COLORS

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
GRAPHICS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "graphics"))
OBJECT_DIR   = os.path.join(GRAPHICS_DIR, "objects")     # old drop-in folder for Tiled objects
ASSET_DIR    = OBJECT_DIR                                 # name kept for old code

SPRITES = {
    # ------------------------------------------------------------ RUNNER (character)
    "runner":            {"file": "Runners Animation/pandesal-walk1.png", "color": "runner"},   # static base
    "runner_idle":       {"file": "Runners Animation/pandesal-walk1.png", "fallback": "runner"},
    "runner_run":        {"files": ["Runners Animation/pandesal-walk1.png",
                                   "Runners Animation/pandesal-walk2.png",
                                   "Runners Animation/pandesal-walk3.png",
                                   "Runners Animation/pandesal-walk4.png"],
                            "fps": 10, "loop": True, "fallback": "runner_idle"},
    "runner_jump":       {"files": ["Runners Animation/Pandesal-jump-animation1.png",
                                   "Runners Animation/Pandesal-jump-animation2.png",
                                   "Runners Animation/Pandesal-jump-animation3.png",
                                   "Runners Animation/Pandesal-jump-animation4.png",
                                   "Runners Animation/Pandesal-jump-animation5.png"],
                            "fps": 10, "loop": True, "fallback": "runner_idle"},
    "runner_fall":       {"file": "Runners Animation/Pandesal-jump-animation5.png", "fallback": "runner_jump"},
    "runner_shield":     {"file": "runner/shield.png", "fallback": "runner_idle"},
    "runner_stun":       {"file": "runner/stun.png", "fallback": "runner_idle"},
    "runner_hurt":       {"files": ["Runners Animation/Pandesal-hurt-animation1.png",
                                   "Runners Animation/Pandesal-hurt-animation2.png"],
                                   "fps": 10, "loop": False, "fallback": "runner_stun"},
    "runner_win":        {"file": "runner/win.png", "fallback": "runner_idle"},
    "runner_lose":       {"file": "runner/lose.png", "fallback": "runner_idle"},

    # ------------------------------------------------------------ runner effects
    "shield_bubble":     {"files": ["Runner Assets/shield.png", "Runner Assets/shield2.png", "Runner Assets/shield3.png", "/home/mrrobot/Climb/Climb-main/graphics/Runner Assets/shield4.png"], "fps": 10, "loop": True, "color": "shield"},
    "fx_inverted":       {"file": "/home/mrrobot/Climb/Climb-main/graphics/Runner Assets/left_right2.png", "size": (40, 40), "color": "inversion"},
    "fx_stun_popup":     {"files": ["Runner Assets/stun.png", "Runner Assets/stun2.png"], "fps": 10, "loop": True, "size": (18, 18), "color": "stun"},
    "fx_slowed":         {"file": "Runner Assets/slow.png", "size": (20, 20), "color": "rain_drop"},
    "fx_superjump_bar":  {"file": "Runner Assets/boost.png", "color": "speed"},

    # ------------------------------------------------------------ pickups
    "heart":             {"files": ["Runner Assets/pandesal1.png",
                                   "Runner Assets/pandesal2.png",
                                   "Runner Assets/pandesal3.png"],
                                   "fps": 1, "loop": True, "color": "heart"},
    "heart_empty":       {"file": "Runner Assets/dead_pandesal.png", "color": "heart_empty"},
    "speed":             {"file": "Runner Assets/coffee.png", "color": "speed"},

    # ------------------------------------------------------------ layered cave background
    "cave_backdrop":     {"file": "/home/mrrobot/Climb/Climb-main/data/levels/bagay na makikita sa kweba.png"},
    "bg_layer_1":        {"file": "/home/mrrobot/Climb/Climb-main/data/levels/bg layer 1.png"},
    "bg_layer_2":        {"file": "/home/mrrobot/Climb/Climb-main/data/levels/bg layer 2.png"},
    "bg_layer_3":        {"file": "/home/mrrobot/Climb/Climb-main/data/levels/bg layer 3.png"},

    # ------------------------------------------------------------ level objects
    "goal":              {"file": "/home/mrrobot/Climb (BACKUP)/Climb-main/graphics/General Assets/Cave_exit.png", "color": "goal"},
    "moving_platform":   {"file": "objects/moving_platform.png", "color": "moving_platform"},
    "moving_block":      {"file": "objects/moving_block.png", "color": "moving_block"},
    "small obj":         {"file": "objects/small obj.png"},     # path platforms (Tiled name)
    "med obj":           {"file": "objects/med obj.png"},
    "big obj":           {"file": "objects/big obj.png"},
    "elevator":          {"file": "objects/elevator.png"},
    "rock":              {"files": ["Runner Assets/rock1.png", "Runner Assets/rock2.png", "Runner Assets/rock3.png"], "fps": 6, "loop": True, "color": "rock"},
    "rock_alt":          {"files": ["Runner Assets/rock4.png", "Runner Assets/rock5.png", "Runner Assets/rock6.png"], "fps": 6, "loop": True, "color": "rock"},
    "bounce":            {"files": [
                                "/home/mrrobot/Climb/Climb-main/data/levels/slime.png",
                                "/home/mrrobot/Climb/Climb-main/data/levels/slime.png",
                                "/home/mrrobot/Climb/Climb-main/data/levels/slime.png",
                          ], "fps": 8, "loop": True, "color": "goal"},
    "moss":              {"file": "Runner Assets/moss.png", "color": "moss"},          # moss tile
    "bat":               {"files": ["Runner Assets/bat1.png", "Runner Assets/bat2.png",
                                "Runner Assets/bat3.png", "Runner Assets/bat4.png"],
                          "fps": 8, "loop": True, "color": "moving_spike"},

    # ------------------------------------------------------------ castle traps
    "dart":              {"file": "Runner Assets/trap1.png", "color": "dart"},
    "dart_charge":       {"file": "traps/dart_charge.png", "fallback": "dart_shot"},
    "dart_shot":         {"files": ["Runner Assets/slippers1.png",
                                  "Runner Assets/slipper2.png",
                                  "Runner Assets/slippers3.png",
                                  "Runner Assets/slippers4.png"], "fps": 8, "loop": True, "color": "dart_shot"},

    # ------------------------------------------------------------ caster
    "orb":               {"file": "caster/orb.png", "fps": 6, "color": "orb"},
    "crosshair":         {"file": "ui/crosshair.png"},
    "crosshair_blocked": {"file": "ui/crosshair_blocked.png", "fallback": "crosshair"},
    "projectile":        {"files": ["Runner Assets/water.png", "Runner Assets/water2.png", "Runner Assets/water3.png"], "fps": 5, "loop": True, "color": "projectile"},

    # ------------------------------------------------------------ spell previews (aim visuals)
    "aim_water":         {"file": "", "color": "dirty_water"},
    "aim_stun":          {"file": "Cross Hairs/crosshair2.png", "color": "stun"},
    "aim_bats":          {"file": "aim/bat_row.png", "color": "moving_bat"},
    "aim_zone":          {"file": "aim/bat_zone.png", "color": "moving_bat"},
    "aim_lightning":     {"file": "aim/lightning_column.png", "color": "lightning_warn"},
    "aim_moss":          {"file": "aim/moss_marker.png", "color": "moss"},
    "aim_inversion":     {"file": "Cross Hairs/crosshair6.png", "color": "inversion"},
    "aim_quake":         {"file": "aim/quake_dust.png", "color": "rock"},
    "aim_flare":         {"file": "aim/flare_zone.png", "color": "solar_flare"},
    "aim_typhoon":       {"file": "Runner Assets/cloud.png", "fallback": "rain_drop"},
    "aim_typhoon_cloud": {"file": "Runner Assets/cloud.png", "color": "rain_drop"},

    # ------------------------------------------------------------ spell effects
    "lightning_warn":    {"file": "Runner Assets/lightning6.png", "color": "lightning_warn"},
    "lightning_bolt":    {"files": ["Runner Assets/lightning1.png", "Runner Assets/lightning2.png", "Runner Assets/lightning3.png", "Runner Assets/lightning4.png", "Runner Assets/lightning5.png", "Runner Assets/lightning6.png", "Runner Assets/lightning7.png"], "fps": 7, "loop": False, "color": "lightning"},
    "flare_warn":        {"files": ["Runner Assets/warn_flare1.png", "Runner Assets/warn_flare2.png", "Runner Assets/warn_flare1.png", "Runner Assets/warn_flare2.png", "Runner Assets/warn_flare1.png", "Runner Assets/lightning6.png"], "fps": 16, "loop": True, "color": "solar_flare"},
    "flare_impact":      {"files": ["Runner Assets/flare1.png", "Runner Assets/flare2.png", "Runner Assets/flare3.png", "Runner Assets/flare3.png", "Runner Assets/flare4.png", "Runner Assets/flare1.png"], "fps": 4, "loop": True, "color": "solar_flare"},
    "rain_drop":         {"file": "Runner Assets/raindrop.png", "color": "rain_drop"},
    "rain_overlay":      {"file": "fx/rain_overlay.png"},
    "flood":             {"files": ["Runner Assets/flood1.png", "Runner Assets/flood2.png"], "fps": 2, "loop": True, "color": "flood"},

    # ------------------------------------------------------------ spell icons (spell bar)
    "icon_water":        {"file": "Skill Icons/water_icon.png"},
    "icon_stun":         {"file": "Skill Icons/Stun_icon.png"},
    "icon_bats":         {"file": "Skill Icons/bat_icon.png"},
    "icon_bolt":         {"file": "Skill Icons/lightning_icon.png"},
    "icon_moss":         {"file": "Skill Icons/moss_icon.png"},
    "icon_invert":       {"file": "Skill Icons/invert_icon.png"},
    "icon_quake":        {"file": "Skill Icons/earthQ_icon.png"},
    "icon_flare":        {"file": "Skill Icons/solar_icon.png"},
    "icon_typhoon":      {"file": "Skill Icons/rain_icon.png"},
    "icon_flood":        {"file": "Skill Icons/flood_icon.png"},

    # ------------------------------------------------------------ panels and HUD
    "panel":             {"file": "ui/panel.png"},
    "hud_panel":         {"file": "ui/hud_panel.png", "fallback": "panel"},
    "runner_panel":      {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/board.png", "fallback": "hud_panel"},
    "caster_panel":      {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/board.png", "fallback": "hud_panel"},
    "tooltip":           {"file": "ui/tooltip.png", "fallback": "panel"},
    "effect_banner":     {"file": "ui/effect_banner.png", "fallback": "panel"},
    "menu_panel":        {"file": "ui/menu_panel.png", "fallback": "panel"},
    "gameover_panel":    {"file": "ui/gameover_panel.png", "fallback": "panel"},
    "hud_bar":           {"file": "ui/hud_bar.png"},
    "slot":              {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_skills.png"},
    "slot_selected":     {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_skills2.png", "fallback": "slot"},
    "slot_hover":        {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_skills.png", "fallback": "slot"},
    "slot_empty":        {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_skills.png", "fallback": "slot"},
    "slot_major":        {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_skills.png"},
    "slot_accent":       {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_skills.png"},          # white, tinted per spell
    "skill_bg_tile":     {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_background.png"},
    "button_background": {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/button_background.png"},
    "cooldown_veil":     {"file": "ui/cooldown_veil.png"},
    "bar_bg":            {"file": "ui/bar_bg.png"},
    "bar_fill":          {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/cast.png"},             # white, tinted per bar
    "bar_overlay":       {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/bars.png"},
    "runner_bar_bg":     {"file": "ui/runner_bar_bg.png", "fallback": "bar_bg"},
    "runner_bar_fill":   {"file": "ui/runner_bar_fill.png", "fallback": "bar_fill"},
    "runner_speed_fill":  {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/speed.png", "fallback": "runner_bar_fill"},
    "caster_bar_bg":     {"file": "ui/caster_bar_bg.png", "fallback": "bar_bg"},
    "caster_bar_fill":   {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/cast.png", "fallback": "bar_fill"},
    "banner_strip":      {"file": "ui/banner_strip.png"},         # white, tinted per effect
    "pip_on":            {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/pip_on.png"},
    "pip_off":           {"file": "/home/mrrobot/Climb/Climb-main/graphics/General Assets/bars.png", "fallback": "pip_on"},
    "caster_pip_on":     {"file": "ui/caster_pip_on.png", "fallback": "pip_on"},
    "caster_pip_off":    {"file": "ui/caster_pip_off.png", "fallback": "pip_off"},
    "countdown_bg":      {"file": "ui/countdown_bg.png"},

    # ------------------------------------------------------------ buttons
    "button":            {"file": "objects/big obj.png"},
    "button_hover":      {"file": "ui/button_hover.png", "fallback": "button"},
    "button_selected":   {"file": "ui/button_selected.png", "fallback": "button"},

    # ------------------------------------------------------------ custom menu assets
    "menu_bg_custom":    {"file": "/home/mrrobot/Climb/Climb-main/graphics/Main Menu Assets/Main_Menu_Background.png"},
    "btn_ascend":        {"file": "/home/mrrobot/Climb/Climb-main/graphics/Main Menu Assets/Button_Ascend.png"},
    "btn_guides":        {"file": "/home/mrrobot/Climb/Climb-main/graphics/Main Menu Assets/Button_Guides.png"},
    "btn_exit":          {"file": "/home/mrrobot/Climb/Climb-main/graphics/Main Menu Assets/Button_Exit.png"},

    # ------------------------------------------------------------ menu and game over
    "menu_bg":           {"file": "ui/menu_bg.png"},
    "title":             {"file": "ui/title.png"},
    "banner_runner":     {"file": "ui/banner_runner.png"},
    "banner_caster":     {"file": "ui/banner_caster.png"},
}

_SCALED_MAX = 600      # cache size limit (resized copies change size often, so keep it bounded)
_file_ok = {}          # path -> bool
_raw     = {}          # key  -> list of unscaled frame Surfaces, or None when there is no art
_scaled  = {}          # cache of resized / flipped / placeholder surfaces


# ============================================================ small helpers
def now():
    """Seconds since pygame started. For sprites that animate regardless of game state."""
    return pygame.time.get_ticks() / 1000.0


def _file_exists(path):
    if path not in _file_ok:
        _file_ok[path] = os.path.isfile(path)
    return _file_ok[path]


def _entry_paths(entry):
    if "files" in entry:
        names = entry["files"]
    elif "file" in entry:
        value = entry["file"]
        if isinstance(value, (list, tuple)):
            names = list(value)
        else:
            names = [value]
    else:
        return []

    flat = []
    for name in names:
        if isinstance(name, (list, tuple)):
            flat.extend(name)
        else:
            flat.append(name)
    return [os.path.join(GRAPHICS_DIR, name) if not os.path.isabs(name) else name for name in flat]


def _legacy_path(name):
    return os.path.join(OBJECT_DIR, name + ".png")


def _shade(color, k):
    return tuple(max(0, min(255, int(c * k))) for c in color)


def _size(size):
    return (max(1, int(size[0])), max(1, int(size[1])))


def _color_for(key):
    """Placeholder colour: the first colour found along the fallback chain."""
    seen = set()
    while key and key not in seen:
        seen.add(key)
        entry = SPRITES.get(key, {})
        name = entry.get("color", key)
        if name in COLORS:
            return COLORS[name]
        key = entry.get("fallback")
    return (255, 0, 255)


def _cache_put(ck, surf):
    if len(_scaled) >= _SCALED_MAX:
        _scaled.clear()
    _scaled[ck] = surf
    return surf


# ============================================================ loading
def _load_image(path):
    try:
        image = pygame.image.load(path)
        if pygame.display.get_init() and pygame.display.get_surface() is not None:
            return image.convert_alpha()
        return image
    except pygame.error as err:
        print(f"[sprites] could not read {path}: {err}")
        return None


def _read_entry(entry, paths):
    if "files" in entry:
        frames = [_load_image(p) for p in paths]
        return None if any(f is None for f in frames) else frames
    img = _load_image(paths[0])
    if img is None:
        return None
    count = max(1, int(entry.get("frames", 1)))
    width = img.get_width() // count
    if count == 1 or width < 1:
        return [img]
    return [img.subsurface(pygame.Rect(i * width, 0, width, img.get_height())).copy()
            for i in range(count)]


def _frames(key):
    """Unscaled frames for key (registry entry first, then graphics/objects/key.png), or None."""
    if key in _raw:
        return _raw[key]
    frames = None
    entry = SPRITES.get(key)
    if entry is not None:
        paths = _entry_paths(entry)
        if paths and all(_file_exists(p) for p in paths):
            frames = _read_entry(entry, paths)
    if frames is None and _file_exists(_legacy_path(key)):
        img = _load_image(_legacy_path(key))
        frames = [img] if img is not None else None
    _raw[key] = frames
    return frames


def resolve(key):
    """First name in the fallback chain that has art, or None if nothing has art."""
    seen = set()
    while key and key not in seen:
        seen.add(key)
        if _frames(key) is not None:
            return key
        key = SPRITES.get(key, {}).get("fallback")
    return None


def has(key):
    """True if key (or anything in its fallback chain) has art."""
    return resolve(key) is not None


def legacy_file(name):
    """True if graphics/objects/<name>.png exists (old drop-in object art)."""
    return _file_exists(_legacy_path(name))


def natural_size(key):
    """Size of the first frame of key's art, or None if there is no art."""
    frames = _frames(key)
    return frames[0].get_size() if frames else None


# ============================================================ animation and drawing
def _frame_index(key, t):
    frames = _frames(key)
    count = len(frames)
    if count <= 1:
        return 0
    entry = SPRITES.get(key, {})
    index = int(max(0.0, t) * float(entry.get("fps", 8)))
    if entry.get("loop", True):
        return index % count
    return min(index, count - 1)


def _frame_surface(key, index, size, flip=False):
    ck = (key, index, size, flip)
    surf = _scaled.get(ck)
    if surf is None:
        surf = _frames(key)[index]
        if surf.get_size() != size:
            surf = pygame.transform.scale(surf, size)
        if flip:
            surf = pygame.transform.flip(surf, True, False)
        surf = _cache_put(ck, surf)
    return surf


def _placeholder(key, size):
    ck = ("placeholder", key, size)
    surf = _scaled.get(ck)
    if surf is None:
        color = _color_for(key)
        surf = pygame.Surface(size)
        surf.fill(color)
        pygame.draw.rect(surf, _shade(color, 0.6), surf.get_rect(), 1 if min(size) < 12 else 2)
        surf = _cache_put(ck, surf)
    return surf


def get(key, size, t=0.0):
    """Surface for key stretched to size. A coloured placeholder when there is no art."""
    size = _size(size)
    name = resolve(key)
    if name is None:
        return _placeholder(key, size)
    return _frame_surface(name, _frame_index(name, t), size)


def draw(surface, key, rect, t=0.0, flip=False, feet=False, alpha=255, tint=None):
    """Draw the sprite for key into rect.

    Returns False when there is no art at all, so the caller can draw its own fallback.
    feet=True keeps the sprite's own size and stands it on the bottom of rect.
    tint multiplies the colours (draw the art in white to use it).
    """
    name = resolve(key)
    if name is None:
        return False
    entry = SPRITES.get(name, {})
    index = _frame_index(name, t)
    if feet:
        natural = _frames(name)[index].get_size()
        size = _size(entry["size"]) if entry.get("size") else natural
        img = _frame_surface(name, index, size, flip)
        off_x, off_y = entry.get("offset", (0, 0))
        x = int(round(rect.centerx - size[0] / 2 + off_x))
        y = int(round(rect.bottom - size[1] + off_y))
    else:
        if rect.w <= 0 or rect.h <= 0:
            return True                      # nothing visible to draw
        size = _size((rect.w, rect.h))
        img = _frame_surface(name, index, size, flip)
        x, y = int(rect.x), int(rect.y)
    if tint is not None:
        img = img.copy()
        img.fill((int(tint[0]), int(tint[1]), int(tint[2]), 255), special_flags=pygame.BLEND_RGBA_MULT)
    if alpha < 255:
        img = img.copy()
        img.set_alpha(max(0, int(alpha)))
    surface.blit(img, (x, y))
    return True


def draw_contained(surface, key, rect, t=0.0, alpha=255):
    """Draw a sprite centered in rect without distorting its aspect ratio."""
    name = resolve(key)
    if name is None:
        return False
    frame = _frames(name)[_frame_index(name, t)]
    src_w, src_h = frame.get_size()
    if src_w <= 0 or src_h <= 0 or rect.w <= 0 or rect.h <= 0:
        return True
    scale = min(rect.w / src_w, rect.h / src_h)
    w, h = max(1, int(src_w * scale)), max(1, int(src_h * scale))
    fitted = pygame.Rect(0, 0, w, h)
    fitted.center = rect.center
    return draw(surface, name, fitted, t=t, alpha=alpha)


def draw_block(surface, key, rect, t=0.0, flip=False, feet=False):
    """Like draw(), but when there is no art it draws a coloured block the size of rect."""
    if draw(surface, key, rect, t=t, flip=flip, feet=feet):
        return
    surface.blit(_placeholder(key, _size((rect.w, rect.h))), (int(rect.x), int(rect.y)))


def draw_line(surface, key, p1, p2, width=2):
    """Stretch the sprite for key along the line p1 -> p2. False when there is no art."""
    name = resolve(key)
    if name is None:
        return False
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = max(1, int(round(math.hypot(dx, dy))))
    img = _frame_surface(name, _frame_index(name, now()), (length, max(1, int(width))))
    if dx or dy:
        img = pygame.transform.rotate(img, -math.degrees(math.atan2(dy, dx)))
    mid = (int(round((p1[0] + p2[0]) / 2)), int(round((p1[1] + p2[1]) / 2)))
    surface.blit(img, img.get_rect(center=mid))
    return True


def _report():
    ready = sum(1 for entry in SPRITES.values()
                if all(_file_exists(p) for p in _entry_paths(entry)))
    print(f"[sprites] {ready} of {len(SPRITES)} sprite entries have art; "
          f"the rest use fallbacks or placeholders.")


_report()
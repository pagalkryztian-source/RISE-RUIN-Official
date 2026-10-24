import os
import pygame

from menu import MAP_SELECTION_QUOTES
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MAPS_DIR = os.path.join(ROOT_DIR, "graphics", "Maps Assets")

# Set these to the real file names in "graphics/Maps Assets".
BACKGROUND_FILE = "background_map.jpeg"
LOGO_FILE = "Maps_logo.png"
BUTTON_MAP1_FILE = "button_map1.png"
BUTTON_COMING_SOON_FILE = "button_map2.png"

# The layout is authored in pixels of the 1024x575 reference image
# and scaled to the actual window, so everything stays aligned at any size.
REF_W, REF_H = 1024, 575
SX = WINDOW_WIDTH / REF_W
SY = WINDOW_HEIGHT / REF_H

LOGO_CENTER = (393, 346)
LOGO_BOX = (240, 80)

BUTTON_BOX = (225, 64)
BUTTON_CENTER_X = 683
BUTTON_CENTERS_Y = (222, 299, 376)

QUOTE_CENTER_Y = 545
QUOTE_FONT_SIZE = max(8, round(16 * SY))


def to_window(x, y):
    return round(x * SX), round(y * SY)


def resolve_asset(filename):
    """Resolve a requested asset name against the actual file extensions in the art folder."""
    stem, ext = os.path.splitext(filename)
    candidates = [filename]

    if ext:
        candidates.extend([
            f"{stem}.png",
            f"{stem}.jpg",
            f"{stem}.jpeg",
        ])
    else:
        candidates = [
            f"{filename}.png",
            f"{filename}.jpg",
            f"{filename}.jpeg",
        ]

    for candidate in candidates:
        path = os.path.join(MAPS_DIR, candidate)
        if os.path.exists(path):
            return candidate

    return filename


def load_fitted(filename, ref_box, smooth=False):
    """Load an image and scale it to fit inside ref_box (reference pixels), keeping its aspect ratio."""
    resolved = resolve_asset(filename)
    image = pygame.image.load(os.path.join(MAPS_DIR, resolved)).convert_alpha()
    box_w, box_h = to_window(*ref_box)
    scale = min(box_w / image.get_width(), box_h / image.get_height())
    size = (max(1, round(image.get_width() * scale)), max(1, round(image.get_height() * scale)))
    resize = pygame.transform.smoothscale if smooth else pygame.transform.scale
    return resize(image, size)


class MapSelectionButton:
    def __init__(self, ref_center, filename, interactive, hover_scale=0.90):
        self.image = load_fitted(filename, BUTTON_BOX)
        self.rect = self.image.get_rect(center=to_window(*ref_center))
        self.interactive = interactive
        self.hover_scale = hover_scale
        self.current_scale = 1.0

    def update(self, dt):
        hovered = self.interactive and self.rect.collidepoint(pygame.mouse.get_pos())
        target_scale = self.hover_scale if hovered else 1.0
        self.current_scale += (target_scale - self.current_scale) * min(1.0, dt * 15.0)

    def clicked(self, event):
        return (
            self.interactive
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        size = (max(1, round(self.rect.width * self.current_scale)), max(1, round(self.rect.height * self.current_scale)))
        scaled = pygame.transform.scale(self.image, size)
        surface.blit(scaled, scaled.get_rect(center=self.rect.center))


class ReturnButton:
    def __init__(self, x, y, text="Return", hover_scale=0.95):
        self.text = text
        self.font = pygame.font.SysFont("monospace", max(9, round(14 * SY)), bold=True)
        self.base_label = self.font.render(text, True, (245, 242, 236))
        self.hover_scale = hover_scale
        self.current_scale = 1.0
        self.base_rect = self.base_label.get_rect(topleft=(x, y))
        self.rect = self.base_rect.inflate(14, 8)

    def update(self, dt):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        target_scale = self.hover_scale if hovered else 1.0
        self.current_scale += (target_scale - self.current_scale) * min(1.0, dt * 18.0)
        if abs(target_scale - self.current_scale) < 0.01:
            self.current_scale = target_scale

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        scaled = pygame.transform.scale(
            self.base_label,
            (
                max(1, int(self.base_label.get_width() * self.current_scale)),
                max(1, int(self.base_label.get_height() * self.current_scale)),
            ),
        )
        scaled_rect = scaled.get_rect(topleft=self.base_rect.topleft)
        surface.blit(scaled, scaled_rect)


class MapSelectionScene:
    def __init__(self, game):
        self.game = game

        background = pygame.image.load(os.path.join(MAPS_DIR, BACKGROUND_FILE)).convert()
        self.background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.logo = load_fitted(LOGO_FILE, LOGO_BOX, smooth=True)
        self.logo_rect = self.logo.get_rect(center=to_window(*LOGO_CENTER))

        self.map_button_1 = MapSelectionButton((BUTTON_CENTER_X, BUTTON_CENTERS_Y[0]), BUTTON_MAP1_FILE, interactive=True)
        self.map_button_2 = MapSelectionButton((BUTTON_CENTER_X, BUTTON_CENTERS_Y[1]), BUTTON_COMING_SOON_FILE, interactive=False)
        self.map_button_3 = MapSelectionButton((BUTTON_CENTER_X, BUTTON_CENTERS_Y[2]), BUTTON_COMING_SOON_FILE, interactive=False)
        self.buttons = (self.map_button_1, self.map_button_2, self.map_button_3)

        self.return_button = ReturnButton(12, 8, text="Return")

        self.font = pygame.font.SysFont("monospace", QUOTE_FONT_SIZE, bold=True)
        self.quotes = list(MAP_SELECTION_QUOTES)
        self.quote_index = 0
        self.quote_timer = 0.0
        self.quote_interval = 5.0

    def handle_event(self, event):
        from sounds import play

        if self.return_button.clicked(event):
            play("ui_button_click")
            self.game.show_menu()
            return

        if self.map_button_1.clicked(event):
            play("ui_button_click")
            self.game.start_match({"runner": "runner", "caster": "caster"})
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            play("ui_button_click")
            self.game.show_menu()

    def update(self, dt):
        for button in self.buttons:
            button.update(dt)
        self.return_button.update(dt)

        self.quote_timer += dt
        if self.quote_timer >= self.quote_interval:
            self.quote_timer = 0.0
            self.quote_index = (self.quote_index + 1) % len(self.quotes)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.logo, self.logo_rect)

        self.return_button.draw(surface)

        for button in self.buttons:
            button.draw(surface)

        line = self.font.render(self.quotes[self.quote_index], False, (245, 242, 236))
        surface.blit(line, line.get_rect(center=(WINDOW_WIDTH // 2, round(QUOTE_CENTER_Y * SY))))
"""Main menu layout with a configurable background video and logo."""
import os
import textwrap
import time

from settings import *
import assets
import sounds
from ui import fit_text, draw_panel, text_width

try:
    import cv2
except ImportError:  # pragma: no cover - optional dependency for MP4 playback
    cv2 = None

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MENU_ART = {
    "background_video": os.path.join(ROOT_DIR, "graphics", "Main Menu Assets", "Background_video_MainMenu.mp4"),
    "background_fallback": os.path.join(ROOT_DIR, "graphics", "Main Menu Assets", "Main_Menu_Background.png"),
    "intro_video": os.path.join(ROOT_DIR, "graphics", "Intro Video", "Game_intro.mp4"),
    "intro_audio": os.path.join(ROOT_DIR, "graphics", "Intro Video", "sound intro.mp3"),
    "logo_path": os.path.join(ROOT_DIR, "graphics", "Main Menu Assets", "logo.png"),
    "logo_scale": 0.35,
    "logo_offset": (23, 35),
    "button_offset_x": 65,
    "button_offset_y": 140,
    "button_spacing_y": 32,
}

STORY_SEGMENTS = (
    "We are all runners, chasing dreams through storms we cannot control and battles we never asked for. No typhoon, flood, or earthquake can stop those who refuse to surrender to life's hardships.\n\nFor it is not the absence of storms that brings us to the top, but the strength to keep climbing when the whole world trembles beneath our feet.",
    "We are sometimes the Casters, consumed by envy, blinded by greed, or corrupted by power. Sometimes, those meant to protect us sacrifice our lives for their own gain.\n\nNot every villain is born evil. Some are shaped by a world that leaves them choosing between becoming the monster or being destroyed by it.",
)

MAP_SELECTION_QUOTES = (
    "Every climb begins with a reason to keep going.",
    "Not every hand will help you climb.",
    "Some storms cannot be avoided. Only survived.",
    "One more jump. One less regret.",
    "Surviving is its own kind of victory.",
    "The higher you climb, the harder they try to stop you.",
    "Your hardest days are not your final days.",
    "Sometimes, the goal is simply to make it home.",
    "You may never know who is casting the next spell.",
    "No storm lasts forever. Keep climbing.",
)


class VideoBackground:
    def __init__(self, video_path, fallback_path, size, loop=True, force_timing=False):
        self.video_path = video_path
        self.fallback_path = fallback_path
        self.size = size
        self.loop = loop
        self.force_timing = force_timing
        self.capture = None
        self.current_frame = None
        self.finished = False
        self.frame_interval = 1.0 / 24.0
        self.clock = 0.0
        self._fallback_surface = self._load_static_surface(fallback_path)
        self._playback_started = None
        self._duration_seconds = None

        if cv2 is not None and os.path.exists(video_path):
            self.capture = cv2.VideoCapture(video_path)
            if not self.capture.isOpened():
                self.capture = None
            else:
                fps = self.capture.get(cv2.CAP_PROP_FPS)
                frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
                if fps and frames:
                    self._duration_seconds = float(frames) / float(fps)

        if self.capture is not None:
            self.current_frame = self._read_frame()

        if self.current_frame is None and self._fallback_surface is not None:
            self.current_frame = self._fallback_surface

    def start(self):
        if self._playback_started is None:
            self._playback_started = time.monotonic()

    def _load_static_surface(self, path):
        if not os.path.exists(path):
            return None
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            return None

    def _read_frame(self):
        if self.capture is None:
            return self.current_frame

        ok, frame = self.capture.read()
        if not ok or frame is None:
            if self.loop:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = self.capture.read()
                if not ok or frame is None:
                    return self._fallback_surface
            else:
                self.finished = True
                if self.capture is not None:
                    self.capture.release()
                    self.capture = None
                return self._fallback_surface or self.current_frame

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = pygame.image.frombuffer(frame.tobytes(), (frame.shape[1], frame.shape[0]), "RGB")
        return image.convert_alpha() if image.get_alpha() is not None else image.convert()

    def update(self, dt):
        if self.finished:
            return

        if self.force_timing and self.capture is not None:
            if self._playback_started is None:
                self.start()

            elapsed = time.monotonic() - self._playback_started
            if self._duration_seconds is not None and elapsed >= self._duration_seconds:
                self.finished = True
                self.capture.release()
                self.capture = None
                return

            target_msec = min(elapsed * 1000.0, (self._duration_seconds or elapsed) * 1000.0)
            pos_msec = self.capture.get(cv2.CAP_PROP_POS_MSEC)
            if target_msec > pos_msec + 30:
                self.capture.set(cv2.CAP_PROP_POS_MSEC, target_msec)
                self.current_frame = self._read_frame()
            return

        self.clock += dt
        if self.clock >= self.frame_interval:
            self.clock = 0.0
            self.current_frame = self._read_frame()

    def draw(self, surface):
        if self.current_frame is None:
            if self._fallback_surface is not None:
                surface.blit(pygame.transform.scale(self._fallback_surface, surface.get_size()), (0, 0))
            else:
                surface.fill(COLORS["bg"])
            return

        scaled = pygame.transform.scale(self.current_frame, surface.get_size())
        surface.blit(scaled, (0, 0))


class IntroScene:
    def __init__(self, game):
        self.game = game
        self.background = VideoBackground(MENU_ART["intro_video"], MENU_ART["background_fallback"], (WINDOW_WIDTH, WINDOW_HEIGHT), loop=False, force_timing=True)
        self.background.start()
        self.skip_rect = pygame.Rect(WINDOW_WIDTH - 82, 12, 68, 20)
        self._transitioning = False
        self._intro_sound = None
        self._start_intro_audio()

    def _start_intro_audio(self):
        audio_path = MENU_ART.get("intro_audio")
        if not audio_path or not os.path.exists(audio_path):
            return
        try:
            if pygame.mixer.get_init() is not None:
                self._intro_sound = pygame.mixer.Sound(audio_path)
                self._intro_sound.set_volume(0.85)
                self._intro_sound.play()
        except pygame.error:
            self._intro_sound = None

    def _go_to_menu(self):
        if self._transitioning:
            return
        self._transitioning = True
        try:
            if self._intro_sound is not None:
                self._intro_sound.stop()
            if pygame.mixer.get_init() is not None:
                pygame.mixer.music.stop()
        except pygame.error:
            pass
        self.game.show_menu()

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.skip_rect.collidepoint(event.pos):
                sounds.play("ui_button_click")
                self._go_to_menu()
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
            sounds.play("ui_button_click")
            self._go_to_menu()

    def update(self, dt):
        if self._transitioning:
            return

        self.background.update(dt)

        if self.background.finished:
            self._go_to_menu()
            return

    def draw(self, surface):
        self.background.draw(surface)

        base_rect = self.skip_rect.copy()
        hover = base_rect.collidepoint(pygame.mouse.get_pos())
        if hover:
            scale = 1.06
            scaled = pygame.Rect(
                int(base_rect.centerx - base_rect.width * scale / 2),
                int(base_rect.centery - base_rect.height * scale / 2),
                int(base_rect.width * scale),
                int(base_rect.height * scale),
            )
            rect = scaled
        else:
            rect = base_rect

        pygame.draw.rect(surface, (18, 18, 18, 180) if not hover else (30, 30, 30, 220), rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), rect.inflate(-2, -2), 2, border_radius=6)
        fit_text(surface, "SKIP", rect, (255, 255, 255), max_size="body")


class ImageButton:
    def __init__(self, topleft_pos, asset_key, scale_factor=1.12):
        self.topleft_pos = topleft_pos
        self.asset_key = asset_key
        self.scale_factor = scale_factor

        natural = assets.natural_size(asset_key)
        if natural:
            self.base_w, self.base_h = natural
        else:
            self.base_w, self.base_h = (90, 24)

        self.current_scale = 1.0

    def get_rect(self):
        w = int(self.base_w * self.current_scale)
        h = int(self.base_h * self.current_scale)
        return pygame.Rect(self.topleft_pos[0], self.topleft_pos[1], w, h)

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        rect = self.get_rect()

        target_scale = self.scale_factor if rect.collidepoint(mouse_pos) else 1.0
        self.current_scale += (target_scale - self.current_scale) * min(1.0, dt * 15.0)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.get_rect().collidepoint(event.pos)
        return False

    def draw(self, surface):
        rect = self.get_rect()
        assets.draw(surface, self.asset_key, rect)


class MenuScene:
    def __init__(self, game):
        self.game = game
        pygame.mouse.set_visible(True)

        self.story_index = 0
        self.story_segment_duration = 20.0
        self.story_type_duration = 2.5
        self.story_timer = 0.0
        self.story_panel = pygame.Rect(330, 46, 200, 165)
        self.guide_open = False
        self.guide_index = 0
        self.guide_images = [self._load_guide_image("Guides_Screen.jpeg"), self._load_guide_image("Guides_Screen2.jpeg")]

        self.background = VideoBackground(
            MENU_ART["background_video"],
            MENU_ART["background_fallback"],
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            loop=True,
            force_timing=False,
        )

        self.logo_surface = self._load_logo()
        self.logo_rect = self._build_logo_rect()

        start_x = MENU_ART["button_offset_x"]
        start_y = MENU_ART["button_offset_y"]
        spacing_y = MENU_ART["button_spacing_y"]

        self.btn_ascend = ImageButton((start_x, start_y), "btn_ascend")
        self.btn_guides = ImageButton((start_x, start_y + spacing_y), "btn_guides")
        self.btn_exit = ImageButton((start_x, start_y + (spacing_y * 2)), "btn_exit")

    def _story_visible_text(self):
        text = STORY_SEGMENTS[self.story_index]
        if self.story_timer < self.story_type_duration:
            visible_chars = int((self.story_timer / self.story_type_duration) * len(text))
            return text[:visible_chars]
        return text

    def _draw_story_panel(self, surface):
        text_rect = pygame.Rect(self.story_panel.left + 8, self.story_panel.top + 8,
                                self.story_panel.width - 16, self.story_panel.height - 16)
        visible = self._story_visible_text()
        lines = []
        for paragraph in visible.splitlines():
            if not paragraph:
                lines.append("")
                continue
            lines.extend(textwrap.wrap(paragraph, width=34, break_long_words=False, break_on_hyphens=False))

        line_height = 15
        y = text_rect.top
        for line in lines:
            if not line:
                y += line_height // 2
                continue
            img = pygame.font.Font(None, 11).render(line, True, (245, 242, 236))
            surface.blit(img, (text_rect.left, y))
            y += line_height

    def _advance_story(self):
        self.story_index = (self.story_index + 1) % len(STORY_SEGMENTS)
        self.story_timer = 0.0

    def _load_guide_image(self, filename):
        path = os.path.join(ROOT_DIR, "graphics", "Guides", filename)
        if not os.path.exists(path):
            return None
        try:
            return pygame.image.load(path).convert_alpha()
        except pygame.error:
            return None

    def _guide_current_image(self):
        if not self.guide_images:
            return None
        current = self.guide_images[self.guide_index]
        return current if current is not None else self.guide_images[0]

    def _guide_image_rect(self):
        image = self._guide_current_image()
        if image is None:
            return None

        source_w, source_h = image.get_size()
        ratio = min(WINDOW_WIDTH / source_w, WINDOW_HEIGHT / source_h)
        new_w = max(1, int(source_w * ratio))
        new_h = max(1, int(source_h * ratio))
        x = (WINDOW_WIDTH - new_w) // 2
        y = (WINDOW_HEIGHT - new_h) // 2
        return pygame.Rect(x, y, new_w, new_h)

    def _guide_text_rect(self, text, x, y):
        pad_x = 12
        pad_y = 8
        return pygame.Rect(x, y, text_width(text, "body") + pad_x * 2, 14 + pad_y * 2)

    def _guide_next_rect(self):
        text = "NEXT"
        w = text_width(text, "body") + 12
        h = 14
        return pygame.Rect(WINDOW_WIDTH - w - 70, 14, w, h)

    def _guide_back_rect(self):
        text = "BACK"
        w = text_width(text, "body") + 12
        h = 14
        return pygame.Rect(57, 10, w, h)

    def _guide_return_rect(self):
        img_rect = self._guide_image_rect()
        if img_rect is None:
            return None

        text = "RETURN"
        label_w = text_width(text, "body") + 12
        label_h = 14
        x = (WINDOW_WIDTH - label_w) // 2
        y = WINDOW_HEIGHT - 30
        return pygame.Rect(x, y, label_w, label_h)

    def _load_logo(self):
        if not os.path.exists(MENU_ART["logo_path"]):
            return None
        try:
            image = pygame.image.load(MENU_ART["logo_path"]).convert_alpha()
            return image
        except pygame.error:
            return None

    def _build_logo_rect(self):
        if self.logo_surface is None:
            return pygame.Rect(0, 0, 0, 0)

        scale = MENU_ART["logo_scale"]
        width = max(1, int(self.logo_surface.get_width() * scale))
        height = max(1, int(self.logo_surface.get_height() * scale))
        rect = pygame.Rect(0, 0, width, height)
        rect.topleft = MENU_ART["logo_offset"]
        return rect

    def handle_event(self, event):
        if self.guide_open:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.guide_index == 0:
                    rect = self._guide_next_rect()
                    if rect.collidepoint(event.pos):
                        sounds.play("ui_button_click")
                        self.guide_index = 1
                        return
                elif self.guide_index == 1:
                    rect = self._guide_back_rect()
                    if rect.collidepoint(event.pos):
                        sounds.play("ui_button_click")
                        self.guide_index = 0
                        return

                rect = self._guide_return_rect()
                if rect and rect.collidepoint(event.pos):
                    sounds.play("ui_button_click")
                    self.guide_open = False
                    self.guide_index = 0
                    return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sounds.play("ui_button_click")
                self.guide_open = False
                self.guide_index = 0
                return
            return

        if self.btn_ascend.clicked(event):
            sounds.play("ui_button_click")
            self.game.show_map_selection()
        elif self.btn_guides.clicked(event):
            sounds.play("ui_button_click")
            self.guide_open = True
            self.guide_index = 0
        elif self.btn_exit.clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sounds.play("ui_button_click")
            self.game.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            sounds.play("ui_button_click")
            self.game.show_map_selection()

    def update(self, dt):
        self.background.update(dt)
        self.btn_ascend.update(dt)
        self.btn_guides.update(dt)
        self.btn_exit.update(dt)

        self.story_timer += dt
        if self.story_timer >= self.story_segment_duration:
            self._advance_story()

    def _draw_guides_screen(self, surface):
        image = self._guide_current_image()
        if image is None:
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        image_rect = self._guide_image_rect()
        if image_rect is not None:
            scaled = pygame.transform.smoothscale(image, image_rect.size)
            surface.blit(scaled, image_rect.topleft)

        def draw_text_button(label, rect, hover):
            pad = 2
            bg_rect = pygame.Rect(rect.left - pad, rect.top - pad, rect.width + pad * 2, rect.height + pad * 2)
            if hover:
                bg_rect = pygame.Rect(
                    int(bg_rect.centerx - bg_rect.width * 1.06 / 2),
                    int(bg_rect.centery - bg_rect.height * 1.06 / 2),
                    int(bg_rect.width * 1.06),
                    int(bg_rect.height * 1.06),
                )
            pygame.draw.rect(surface, (255, 255, 255), bg_rect, border_radius=2)
            fit_text(surface, label, bg_rect, (0, 0, 0), max_size="body")

        if self.guide_index == 0:
            next_rect = self._guide_next_rect()
            hover = next_rect.collidepoint(pygame.mouse.get_pos())
            draw_text_button("NEXT", next_rect, hover)
        elif self.guide_index == 1:
            back_rect = self._guide_back_rect()
            hover = back_rect.collidepoint(pygame.mouse.get_pos())
            draw_text_button("BACK", back_rect, hover)

        rect = self._guide_return_rect()
        if rect is not None:
            hover = rect.collidepoint(pygame.mouse.get_pos())
            if hover:
                scaled_rect = pygame.Rect(
                    int(rect.centerx - rect.width * 1.12 / 2),
                    int(rect.centery - rect.height * 1.12 / 2),
                    int(rect.width * 1.12),
                    int(rect.height * 1.12),
                )
                fit_text(surface, "RETURN", scaled_rect, (0, 0, 0), max_size="body")
            else:
                fit_text(surface, "RETURN", rect, (0, 0, 0), max_size="body")

    def draw(self, surface):
        self.background.draw(surface)

        if self.logo_surface is not None:
            logo = pygame.transform.scale(self.logo_surface, self.logo_rect.size)
            surface.blit(logo, self.logo_rect.topleft)

        if self.guide_open:
            self._draw_guides_screen(surface)
            return

        self._draw_story_panel(surface)

        self.btn_ascend.draw(surface)
        self.btn_guides.draw(surface)
        self.btn_exit.draw(surface)
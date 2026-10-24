"""The Game owns the window and switches between scenes (menu <-> match). Maps are loaded with pytmx."""
from os.path import join
from pytmx.util_pygame import load_pygame
from settings import *
from level import Level
from menu import MenuScene
from game_scene import GameScene
from maps_selection import MapSelectionScene
import sounds


class Game:
    def __init__(self):
        pygame.init()
        sounds.init()                                   # initialise audio mixer
        pygame.display.set_caption("Castle Climb - Runner vs Caster")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.tmx_maps = {file: load_pygame(join('..', 'data', 'levels', file)) for _, file in LEVELS}
        self.show_intro()

    def show_intro(self):
        sounds.stop_all_sfx()
        sounds.set_menu_shield_max(True)
        sounds.stop_bgm()
        from menu import IntroScene
        self.scene = IntroScene(self)

    def new_level(self, index=0):
        name, file = LEVELS[index]
        return Level(self.tmx_maps[file], name)

    def show_menu(self):
        # stop any leftover game sound effects and set menu shield volume
        sounds.stop_all_sfx()
        sounds.set_menu_shield_max(True)
        sounds.play_bgm("bgm_menu")
        self.scene = MenuScene(self)

    def show_map_selection(self):
        # Allow the button click sound to finish before transitioning.
        # Stopping all SFX here cuts off the click that was just triggered.
        self.scene = MapSelectionScene(self)

    def start_match(self, roles):
        # restore shield volume to its game value and start game BGM
        sounds.set_menu_shield_max(False)
        sounds.play_bgm("bgm_game")
        self.scene = GameScene(self, roles)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 1 / 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                else:
                    self.scene.handle_event(event)
            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

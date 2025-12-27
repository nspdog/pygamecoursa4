import os
import pygame
from scenes.scene import Scene

class IntroScene(Scene):
    def __init__(self, scene_manager):
        super().__init__("Intro", scene_manager)
        self.images = []
        self.current_ind = 0
        self.backgroud_sound = None
        self.display_duration = 5  # Максимальная длительность показа картинки
        self.current_display_time = 0

    def on_enter(self):
        for filename in os.listdir("assets/image/intro"):
            img = pygame.image.load(f"assets/image/intro/{filename}")
            self.images.append(img)

        self.backgroud_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "assets/audio/Белка в колесе (Hamster Wheel).mp3")
        self.backgroud_sound.play()

    def on_exit(self):
        self.images.clear()
        self.backgroud_sound.stop()
        self.current_display_time = 0
        self.current_ind = 0

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Пропуск интро - переход к игровой сцене
                self.ref_scene_manager.change_scene("Game")

    def update(self, dt):
        self.current_display_time += dt
        if self.current_display_time >= self.display_duration:
            self.current_display_time = 0
            if self.current_ind < len(self.images) - 1:
                self.current_ind += 1
            else:
                self.ref_scene_manager.change_scene("Game")

    def render(self, surface: pygame.Surface):
        surface.blit(self.images[self.current_ind], (0, 0))



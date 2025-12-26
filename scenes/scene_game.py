from typing import List, Optional
import pygame

import settings
from game_objects.camera import Camera
from game_objects.gobject import GameObject
from game_objects.ground import Map
from game_objects.player import Player, House, Tree
from scenes.scene import Scene
from game_objects.world import WorldMap
from widgets.text_label import TextLabel

class Romb:
    def __init__(self, center: tuple[float, float], size: tuple[int, int]):
        self.center = center
        self.size = size
        self._corners = [
            (center[0] - size[0]//2, center[1]), #left
            (center[0], center[1] - size[1]//2), #top
            (center[0] + size[0]//2, center[1]), #right
            (center[0], center[1] + size[1]//2) #botom
        ]

    def split(self):
        ns = (self.size[0]//2, self.size[1]//2)
        w = Romb((self.center[0] - self.size[0]//4, self.center[1]), ns)
        e = Romb((self.center[0] + self.size[0] // 4, self.center[1]), ns)
        n = Romb((self.center[0],self.center[1] - self.size[1]//4), ns)
        s = Romb((self.center[0],self.center[1] + self.size[1]//4), ns)
        return [w, e, n, s]


    def draw(self, surface: pygame.Surface):
        pygame.draw.lines(surface, (255, 0, 255, 255),True, self._corners)

from widgets.frame import FrameWidget
class GameScene(Scene):
    def __init__(self, scene_manager):
        super().__init__("Game", scene_manager)

        self.frame = FrameWidget(pygame.Rect((100, 100), (500, 500)),"Frame",
                    "assets/image/ui/frame.png",
                    pygame.Rect((10, 10), (90, 104)),
                    pygame.Rect((110, 10), (90, 40)))

        self.label = TextLabel("Hello! Здесь предствален большой текст", 200, 600, 600, 250,50)

        self.world = Map(60, 60)
        self.player: Optional['Player'] = Player(self.world)

        self.camera = Camera(0, 0)
        self.camera.attach(self.player)

        self.r = Romb((100, 100), settings.tile_size)

        self.l = self.r.split()
        self.l1 = self.l[0].split()

        self.world.add_dinamic_object(self.player, 6, 5)
        self.world.add_static_object(Tree(), 5, 6)
        self.world.add_static_object(Tree(), 2, 2)
        self.world.add_static_object(Tree(), 6, 1)
        self.world.add_static_object(House(), 8, 8)


    def on_enter(self) -> None:
        pass

    def handle_events(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.ref_scene_manager.change_scene("Main menu")

        if self.player:
            self.player.handle_event(event)

    def update(self, delta_time: float):
        if self.world:
            self.world.update(delta_time)

        if self.camera:
            self.camera.update(delta_time)



    def render(self, surface: pygame.Surface) -> None:

        if self.world:
            self.world.render(surface, self.camera.offset)

        if self.camera:
            self.camera.render(surface)
        self.r.draw(surface)

        for l in self.l:
            l.draw(surface)
        for l in self.l1:
            l.draw(surface)

        self.frame.render(surface)
        self.label.render(surface)

    def on_exit(self):
        if self.world:
            del self.world

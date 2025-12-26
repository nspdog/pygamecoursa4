from typing import Optional

import pygame

from game_objects.component_character_stats import CharacterStatsComponent
from game_objects.component_controller import PlayerControllerComponent
from game_objects.component_image import ImageComponent
from game_objects.component_transform import TransformComponent
from game_objects.component_animation import CharacterAnimationComponent
from game_objects.component_collider import ColliderComponent
from game_objects.gobject import GameObject
import utils


class Player(GameObject):
    def __init__(self, map_ref):
        super().__init__("Player")
        self.add_component(TransformComponent())
        self.add_component(CharacterStatsComponent(name="Лесник"))
        self.add_component(ColliderComponent(size=(50, 50), stride= 20))
        self.add_component(PlayerControllerComponent(map_ref))
        self.add_component(
            CharacterAnimationComponent("assets/image/GameObjects/Character/Forester",
                                        (-75, -180)))

    def render(self, surface: pygame.Surface, camera_offset: Optional[pygame.math.Vector2] = None) -> None:
        super().render(surface, camera_offset)

    def update(self, delta_time: float) -> None:
        super().update(delta_time)

        transform = self.get_component("transform")
        if transform:
            pos = transform.screen_position
            iso = utils.iso_to_cart(pos.x, pos.y)
            print(f"\r {pos} {iso}", end="")


class House(GameObject):
    def __init__(self):
        super().__init__("House")
        self.add_component(TransformComponent(8, 8))
        self.add_component(ImageComponent("assets/image/GameObjects/Home.png",
                                          (-0, -500)))


class Tree(GameObject):
    def __init__(self, row = 0, col =0):
        super().__init__("Tree")
        self.add_component(TransformComponent(row, col))
        self.add_component(ImageComponent("assets/image/GameObjects/Tree/Tree.png",
                                          (-140, -280)))
        self.add_component(ColliderComponent(size=(50, 50)))


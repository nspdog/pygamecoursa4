from typing import Optional

import pygame.math

import game_objects.gobject
import settings
import utils
from game_objects.component_transform import TransformComponent


class Camera:
    def __init__(self, row, col):
        screen_offset = pygame.math.Vector2(settings.screen_width // 2, settings.screen_height // 2)
        world_offset = utils.cart_to_iso(row, col)

        self.is_following = False

        self.offset = world_offset - screen_offset
        self.target: Optional['TransformComponent'] = None

    def attach(self, game_object: game_objects.gobject.GameObject):
        transform = game_object.get_component("transform")
        if transform:
            self.target = transform
            self.target.on_event(TransformComponent.EventType.POSITION_CHANGED, self.center_on_target)
            self.center_on_target()

    def center_on_target(self):
        """Мгновенно центрирует камеру на цели"""
        if self.target:
            world_pos = self.target.get_screen_position()
            screen_center = pygame.math.Vector2(
                settings.screen_width // 2,
                settings.screen_height // 2
            )
            self.offset = world_pos - screen_center

    def update_position(self):
        if self.target:
            world_offset = transform.get_screen_position()
            screen_offset = pygame.math.Vector2(settings.screen_width // 2, settings.screen_height // 2)
            self.offset = world_offset - screen_offset

    def render(self, surface):
        pass

    def update(self, dt):
        if self.target:
            pass




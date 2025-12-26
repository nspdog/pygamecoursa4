from typing import Optional

from game_objects.component import Component
from game_objects.component_transform import Direction
from game_objects.component_controller import  ControllerComponent
from game_objects.component_transform import  TransformComponent
from game_objects.frame_sequence import FrameSequence

import pygame
import os

from game_objects.movement_state import MovementState


class CharacterAnimationComponent(Component):
    def __init__(self, path,  offset: tuple = (0, 0)):
        super().__init__("animation")

        #Анимация, направление, изображение, текущий кадр
        self.sprite_list: dict[MovementState, dict[Direction, list[(Surface, int)]]] = {}
        self.animations: dict[MovementState, FrameSequence] = {}
        self.surface = None
        self.init_animations(path)

        self.offset = offset

    def on_attach(self, game_object: 'GameObject') -> None:
        super().on_attach(game_object)
        self.controller: ControllerComponent = game_object.get_component("controller")
        self.transform: TransformComponent = game_object.get_component("transform")

    def init_animations(self, path: str):
        for filename in os.listdir(path):
            if not filename.endswith(".png"):
                continue
            character_name, animation_state, direction, frame_number = self.parse_character_filename(filename)
            image_path = f"{path}/{filename}"
            try:
                image = pygame.image.load(image_path).convert_alpha()
                state = MovementState(animation_state)
                direction = Direction(direction)

                if state not in self.sprite_list.keys():
                    self.sprite_list[state] = {}
                if direction not in self.sprite_list[state].keys():
                    self.sprite_list[state][direction] = []

                self.sprite_list[state][direction].append((image, frame_number))
            except pygame.base.error as e:
                print(f"Ошибка при загрузке файла {filename} : {e}")

        for _, directions in self.sprite_list.items():
            for direction, frames in directions.items():
                directions[direction] = sorted(frames, key=lambda x: x[1])

        for state in self.sprite_list.keys():
            if state == MovementState.WALK:
                self.animations[state] = \
                    FrameSequence(state.name, len(self.sprite_list[state][Direction.S]), 0.1333)
            if state == MovementState.IDLE:
                self.animations[state] = \
                    FrameSequence(state.name, len(self.sprite_list[state][Direction.S]), 0.45)
            self.animations[state].run()

    def parse_character_filename(self, filename: str):
        name_without_extension: str = filename.rsplit('.', 1)[0]
        parts: [str] = name_without_extension.split('_')
        if len(parts) != 4:
            raise ValueError(f"Неверный формат имени файла {filename}")

        character_name = parts[0]
        action_type = parts[1]
        direction = parts[2]
        frame_number = int(parts[3])

        return character_name, action_type, direction, frame_number

    def update(self, dt: float):
        super().update(dt)
        state = self.controller.movement_state
        direction = self.transform.direction
        if state in self.sprite_list.keys():
            self.animations[state].update(dt)
            frame = self.animations[state].get_frame()
            self.surface = self.sprite_list[state][direction][frame][0]

    def render(self, surface: pygame.Surface, offset: Optional[pygame.math.Vector2] = None) -> None:
        if self.surface:
            pos = self.transform.get_screen_position() + self.offset - offset
            surface.blit(self.surface, pos)






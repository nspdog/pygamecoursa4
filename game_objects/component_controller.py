from typing import Optional

import pygame

import utils
from game_objects.component import Component
from game_objects.component_character_stats import CharacterStatsComponent
from game_objects.component_transform import TransformComponent, Direction
from game_objects.component_collider import ColliderComponent, CollisionBehavior
from game_objects.ground import Map
from pygame.math import Vector2


from game_objects.movement_state import MovementState


class ControllerComponent(Component):
    def __init__(self, map_ref:Map):
        super().__init__("controller")
        # Основные компоненты
        self.transform: Optional['TransformComponent'] = None
        self.stats: Optional['CharacterStatsComponent'] = None
        self.collider: Optional['ColliderComponent'] = None

        self.movement_state = MovementState.IDLE

        self.move_vector = Vector2(0, 0)
        self.test_point: tuple[float, float] = (0, 0)

        self.map_ref:Map = map_ref


    def on_attach(self, game_object: 'GameObject') -> None:
        self.transform = game_object.get_component("transform")
        if not self.transform:
            print("Для ControllerComponent нужен TransformComponent")
        self.stats = game_object.get_component("stats")
        if not self.stats:
            print("Для ControllerComponent нужен CharacterStatsComponent")
        self.collider = game_object.get_component("collider")
        if not self.collider:
            print("Для ControllerComponent нужен ColliderComponent")

    def set_state(self, state: MovementState):
        self.movement_state = state

    def move(self):
        direction = self.transform.direction.to_vector()
        speed = self.stats.base_move_speed
        self.move_vector = direction * speed

        self.set_state(MovementState.WALK)


    def stop(self):
        direction = self.transform.direction.to_vector()
        speed = self.stats.base_move_speed
        self.move_vector = direction * speed
        self.set_state(MovementState.IDLE)

    def run(self):

        direction = self.transform.direction.to_vector()
        speed = self.stats.base_running_speed
        self.move_vector = direction * speed
        self.set_state(MovementState.RUN)


    def set_direction(self, direction: Direction):
        self.transform.set_direction(direction)

    def update(self, delta_time: float) -> None:
        if not self.enabled or not self.transform or not self.stats:
            return

        if ((self.movement_state == MovementState.WALK or
             self.movement_state == MovementState.RUN )
                and self.stats.is_alive):

            self.test_point = self.transform.screen_position + self.transform.direction.to_vector() * 100
            x, y = self.test_point
            r, c = utils.iso_to_cart(x, y)

            if not self.map_ref.is_walkable(r, c):
                return

            for obj in self.map_ref.all_static_objects:
                other = obj.get_component("collider")
                #print(other)
                if other:
                    res = self.collider.check_collision(other)
                    if res and other.behavior == CollisionBehavior.BLOCK:
                        return


            move_x = self.move_vector.x * delta_time
            move_y = (self.move_vector.y * delta_time)/2
            self.transform.move_screen(move_x, move_y)

    def render(self, surface: pygame.Surface, offset: Optional[pygame.math.Vector2] = None) -> None:

        pygame.draw.circle(surface, (255, 255, 0), self.test_point - offset, 5)

class PlayerControllerComponent(ControllerComponent):
    def __init__(self, map_ref):
        super().__init__(map_ref)
        self.move_keys = {
            pygame.K_w: Direction.N,
            pygame.K_s: Direction.S,
            pygame.K_a: Direction.W,
            pygame.K_d: Direction.E
        }
        self.active_keys = set()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key in self.move_keys:
                self.active_keys.add(event.key)
                self._update_movement()
                return True
            elif event.key == pygame.K_SPACE:
                self.movement_state = MovementState.RUN
                self._update_movement()
                return True

        elif event.type == pygame.KEYUP:
            if event.key in self.move_keys and event.key in self.active_keys:
                self.active_keys.remove(event.key)
                self._update_movement()
                return False
            elif event.key == pygame.K_SPACE:
                self.set_state(MovementState.RUN)
                self._update_movement()
                return True

        return False

    def _update_movement(self):
        """Обновляет вектор движения на основе активных клавиш"""

        self.move_vector = pygame.math.Vector2(0, 0)

        for key in self.active_keys:
            if key in self.move_keys:
                self.move_vector += self.move_keys[key].to_vector()
        #self.set_direction(Direction.from_vector(self.move_vector))

        if self.move_vector.length() > 0:
            self.set_direction(Direction.from_vector(self.move_vector))
            if self.movement_state == MovementState.RUN:
                self.run()
            else:
                self.move()
        else:
            self.stop()

class AiControllerComponent(ControllerComponent):
    def __init__(self):
        pass

    def move_to(self):
        pass




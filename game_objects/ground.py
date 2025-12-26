import random
from typing import Dict, Optional, List, Tuple, Set

import pygame

import settings
import utils
from game_objects.camera import Camera
from game_objects.gobject import GameObject
from game_objects.component_collider import CollisionBehavior
from uuid import UUID

class TileType:
    """Тип тайла с его свойствами"""

    def __init__(self, tile_id: int, name: str, walkable: bool, image_path: str = None, walkable_speed: float = 1, ):
        self.tile_id = tile_id
        self.name = name
        self.is_walkable = walkable
        self.walkable_speed = walkable_speed
        self.image_path = image_path
        self.surface: Optional['pygame.surface.Surface'] = None

    def load_image(self):
        self.surface = pygame.image.load(self.image_path).convert_alpha()


class Map:
    def __init__(self, rows, cols, tile_size: tuple = (256, 128)):

        self.tile_size = tile_size  # Размер тайла в пикселях (для спрайтов)

        self.rows = rows
        self.cols = cols
        # Двумерный массив индексов тайлов [y][x]
        self.tile_grid: list[list[int]] = [[0 for _ in range(0, self.cols)] for _ in range(0, self.rows)]
        self.walk_grid: list[list[float]] = [[1 for _ in range(cols)] for _ in range(rows)]
        self.static_objects: list[list[Optional['GameObject']]] = [[None for _ in range(cols)] for _ in range(rows)]

        self.all_static_objects: Set[GameObject] = set()
        self.all_dynamic_objects: Set[GameObject] = set()
        self.render_stack: List[Tuple[UUID, int, GameObject]] = []  # (uuid, z_index, object)

        # Словарь типов тайлов: tile_id -> TileType
        self.tile_types: Dict[float, TileType] = {}

        # Позиция карты в мире (изометрические координаты)
        self._register_tiles()
        self.fill_random_grid(0, 1)



    def is_walkable(self, row: int, col: int) -> bool:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False  # выход за границы карты

        if self.walk_grid[row][col] == 0:
            return False
        return True

    def add_static_object(self, game_object: GameObject, row: int, col: int):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        transform = game_object.get_component("transform")
        if transform:
            transform.set_cart(row, col)
            self.static_objects[row][col] = game_object
            self.all_static_objects.add(game_object)

            if game_object.name == "House":
                for i in range(3):
                    for j in range(3):
                        self.walk_grid[row+i+1][col-j] = 0



    def add_dinamic_object(self, game_object: GameObject, row: int, col: int):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        game_object.get_component("transform").set_cart(row, col)
        self.all_dynamic_objects.add(game_object)

    def _register_tiles(self):
        self.add_tile_type(TileType(0, "Grass", True, "assets/image/Ground/Grass_3.png"))
        self.add_tile_type(TileType(1, "Dirt", True, "assets/image/Ground/Dirt_1.png"))

    def add_tile_type(self, tile_type: TileType):
        """Добавляет тип тайла"""
        self.tile_types[tile_type.tile_id] = tile_type
        tile_type.load_image()

    def set_tile(self, x: int, y: int, tile_id: int):
        """Устанавливает тайл в позицию (x, y)"""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.tile_grid[y][x] = tile_id

    def get_tile(self, x: int, y: int) -> int:
        """Возвращает ID тайла в позиции (x, y)"""
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.tile_grid[y][x]
        return 0

    def fill_random_grid(self, min_range_val: int, max_range_val: int):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tile_grid[row][col] = random.randint(min_range_val, max_range_val)

    def region_to_draw(self, row, col, reg_size):
        r_top_left = max(0, row - reg_size // 2)
        c_top_left = max(0, col - reg_size // 2)
        r_bot_right = min(self.rows, r_top_left + reg_size)
        c_bot_right = min(self.cols, c_top_left + reg_size)

        return r_top_left, c_top_left, r_bot_right, c_bot_right

    def update_render_stack(self, row, col, offset):
        rtl, ctl, rbr, cbr = self.region_to_draw(row, col, 17)
        for r in range(rtl, rbr):
            for c in range(ctl, cbr):
                z = utils.z_stack_value(r, c) - offset.y
                if self.static_objects[r][c]:
                    self.render_stack.append((self.static_objects[r][c].id, z, self.static_objects[r][c]))

        for obj in self.all_dynamic_objects:
            if obj:
                x, y = obj.get_component('transform').screen_position
                z = y - offset.y
                self.render_stack.append((obj.id, z, obj))

        self.render_stack.sort(key=lambda item: item[1])

    def render(self, surface: pygame.Surface, offset: Optional[pygame.math.Vector2] = pygame.math.Vector2(0, 0)):
        map_offset = (self.tile_size[0] // 2, self.tile_size[1] // 2)
        self.offset = -offset - map_offset if offset is not None else self.offset - map_offset
        r, c = utils.iso_to_cart(offset.x + settings.screen_width // 2, offset.y + settings.screen_height // 2)

        self.update_render_stack(r, c, offset)
        reg = self.region_to_draw(r, c, 17)

        for r in range(reg[0], reg[2]):
            for c in range(reg[1], reg[3]):
                id = self.tile_grid[r][c]
                pos = utils.cart_to_iso(r, c)
                surface.blit(self.tile_types[id].surface, self.offset + pos)

        for _, _, obj in self.render_stack:
            if obj:
                obj.render(surface, offset)

        self.render_stack.clear()
        """
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                id = self.tile_grid[r][c]
                pos = utils.cart_to_iso(r, c)

                surface.blit(self.tile_types[id].surface, self.offset + pos)
          """

    def update(self, delta_time):
        for obj in self.all_dynamic_objects:
            obj.update(delta_time)

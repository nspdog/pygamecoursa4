import pygame.math

from game_objects.component import Component


class CharacterStatsComponent(Component):
    """
       Компонент характеристик персонажа (игрок, NPC, враг)
       Содержит все параметры: здоровье, стамина, характеристики и т.д.
    """
    def __init__(self,
                 max_health: float = 100,
                 max_stamina: float = 100,
                 base_move_speed: float = 150.0,
                 name: str = "NoName",
                 info: str = "..."):
        super().__init__("stats")
        self.max_health = max_health
        self.max_stamina = max_stamina
        self.base_move_speed = base_move_speed
        self.base_running_speed = self.base_move_speed * 2
        self.character_name = name
        self.info = info

        self.current_health = self.max_health
        self.current_stamina = self.max_stamina

    def is_alive(self)->bool:
        return self.current_health > 0

    def use_stamina(self, val: float)->bool:
        current_stamina = self.current_stamina - val
        if current_stamina >= 0:
            self.current_stamina = current_stamina
            return True
        print("Не хватает выносливости")
        return False

    def restore_stamina(self, dt):
        current_stamina = self.max_stamina / 100 * dt
        self.current_stamina = min(current_stamina, self.max_stamina)

    def take_damage(self, val: float):
            current_health = self.current_health - val
            if current_health >= 0:
                self.current_health = current_health
                print(f"Персонаж {self.name} получил урон {val}")
                return True
            else:
                current_health = 0
                print(f"Персонаж {self.name} умер")
                return False

    def update(self, dt: float):

        if not self.enabled:
            return

        if self.current_stamina < self.max_stamina:
            self.restore_stamina(dt)






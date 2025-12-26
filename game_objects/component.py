from abc import ABC
from typing import Optional, Callable
import pygame
from enum import Enum


class Component(ABC):
    """
    Базовый компонент, который можно добавлять к GameObject.
    Компоненты добавляют специфическое поведение объектам.
    """

    def __init__(self, name: str):
        self.name = name
        self.game_object: Optional['GameObject'] = None
        self.enabled = True
        # Для событий
        self.event_types: Set[Enum] = set()
        self.event_handlers: Dict[Enum, List[Callable]] = {}

    def register_event_type(self, event_type: Enum) -> None:
        """Зарегистрировать новый тип события для этого компонента"""
        self.event_types.add(event_type)
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

    def on_event(self, event_type, callback: Callable[..., None]):
        if event_type not in self.event_types:
            self.register_event_type(event_type)
        if callback not in self.event_handlers[event_type]:
            self.event_handlers[event_type].append(callback)
        return self

    def off_event(self, event_type, callback: Callable[..., None]) -> 'Component':
        """Отписаться от события"""
        if event_type in self.event_handlers:
            if callback in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(callback)
        return self

    def emit(self, event_type: Enum) -> None:
        if event_type in self.event_handlers:
            for callback in self.event_handlers[event_type][:]:
                callback()

    def on_attach(self, game_object: 'GameObject') -> None:
        """Вызывается при присоединении к GameObject"""
        self.game_object = game_object

    def on_detach(self) -> None:
        """Вызывается при отсоединении от GameObject"""
        self.game_object = None

    def update(self, delta_time: float) -> None:
        """Обновление логики компонента"""
        pass

    def render(self, surface: pygame.Surface, offset: Optional[pygame.math.Vector2] = None) -> None:
        """Отрисовка компонента (необязательная)"""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обработка событий компонентом (необязательная)"""
        return False

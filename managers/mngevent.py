
from enum import Enum, auto

from typing import List, Callable, Dict


class EventType(Enum):
    PLAYER_MOVE = "player move"
    COLLISION = "collision"

class EventManager:
    def __init__(self):
        self._handlers: Dict[EventType, List[Callable]] = {}


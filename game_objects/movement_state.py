from enum import Enum
class MovementState(Enum):
    """Состояния движения персонажа"""
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    PICKUP = "pickup"



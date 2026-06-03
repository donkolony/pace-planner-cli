from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RunTypes(Enum):
    EASY = "easy"
    TEMPO = "tempo"
    LONG_RUN = "long run"
    INTERVAL = "interval"
    REST = "rest"


class Intensity(Enum):
    ZONE_1 = "recovery"
    ZONE_2 = "easy"
    ZONE_3 = "moderate"
    ZONE_4 = "tempo"
    ZONE_5 = "maximum"


@dataclass
class Workout:
    type: RunTypes
    distance: float
    intensity: Intensity
    scheduled_date: datetime = field(default_factory=datetime.now())

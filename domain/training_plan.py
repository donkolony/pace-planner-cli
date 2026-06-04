from dataclasses import dataclass, field
from datetime import datetime, timedelta

from domain.workout import Workout


@dataclass
class TrainingPlan:
    race_date: datetime
    goal_time: timedelta
    starting_mileage: float
    workouts: list[Workout] = field(default_factory=list)

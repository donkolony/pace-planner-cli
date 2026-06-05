from datetime import datetime, timedelta

from domain.workout import Workout, RunTypes, Intensity
from domain.training_plan import TrainingPlan
from services.plan_generator import generate_plan

from pprint import pprint

# Workout i
workout = Workout(
    type=RunTypes.EASY,
    distance=5.0,
    intensity=Intensity.ZONE_2,
    scheduled_date=datetime.now(),
)


# Training plan instance
plan = TrainingPlan(
    race_date=datetime(2025, 10, 1),
    goal_time=timedelta(hours=3, minutes=30),
    starting_mileage=20.0,
    workouts=[workout],
)

target_race_date = datetime(2026, 10, 1)
target_race_time = timedelta(hours=3, minutes=30)
starting_mileage = 20.0

_plan = generate_plan(target_race_date, target_race_time, starting_mileage)


pprint(_plan)

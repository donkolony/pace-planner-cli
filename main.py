from datetime import datetime, timedelta

from domain.workout import Workout, RunTypes, Intensity
from domain.training_plan import TrainingPlan
from services.plan_generator import generate_training_plan

from pprint import pprint

# User Input
target_race_date = datetime(2026, 10, 1)
target_race_time = timedelta(hours=3, minutes=30)
starting_mileage = 20.0

plan = generate_training_plan(target_race_date, target_race_time, starting_mileage)


pprint(plan)

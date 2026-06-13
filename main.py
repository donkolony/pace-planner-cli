from datetime import datetime, timedelta

from domain.workout import Workout, RunTypes, Intensity
from domain.training_plan import TrainingPlan
from services.plan_generator import generate_training_plan

from infrastructure.storage import serialize_training_plan, save_plan_to_local_storage

from pprint import pprint

if __name__ == "__main__":
    # User Input
    target_race_date = datetime(2026, 10, 1)
    target_race_time = timedelta(hours=3, minutes=30)
    starting_mileage = 20.0

    plan = generate_training_plan(target_race_date, target_race_time, starting_mileage)
    save_plan_to_local_storage(plan)

    # pprint(plan)
    # pprint(serialized_plan)

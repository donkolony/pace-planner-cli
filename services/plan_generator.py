from domain.workout import Workout, RunTypes, Intensity
from domain.training_plan import TrainingPlan
from datetime import datetime, timedelta


def generate_plan(
    target_race_date: datetime,
    target_goal_time: timedelta,
    starting_mileage: float,
) -> TrainingPlan:
    # Create a dummy workout
    dummy_workout1 = Workout(
        type=RunTypes.EASY,
        distance=5.0,
        intensity=Intensity.ZONE_1,
        scheduled_date=datetime.now(),
    )

    # Create a training plan
    plan = TrainingPlan(
        race_date=target_race_date,
        goal_time=target_goal_time,
        starting_mileage=starting_mileage,
        workouts=[
            dummy_workout1,
        ],
    )

    return plan

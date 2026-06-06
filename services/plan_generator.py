from domain.workout import Workout, RunTypes, Intensity
from domain.training_plan import TrainingPlan
from domain.templates import BEGINNER_MICROCYCLE

from datetime import datetime, timedelta


def generate_training_plan(
    race_date: datetime,
    goal_time: timedelta,
    starting_mileage: float,
) -> TrainingPlan:

    # 1. Logic
    today = datetime.now()
    total_days = (race_date - today).days
    total_weeks = total_days // 7

    # 2. Empty list to hold the generated works
    generated_workouts = []

    # 3. Loop
    for week in range(total_weeks):
        for day in BEGINNER_MICROCYCLE:
            days_passed = (week * 7) + day
            scheduled_date = today + timedelta(days=days_passed)

            run_type = BEGINNER_MICROCYCLE[day]

            new_workout = Workout(
                type=run_type,
                distance=5.0,  # TODO make dynamic
                intensity=Intensity.ZONE_2,  # TODO make dynamic
                scheduled_date=scheduled_date,
            )

            generated_workouts.append(new_workout)

    # Create a training plan
    plan = TrainingPlan(
        race_date=race_date,
        goal_time=goal_time,
        starting_mileage=starting_mileage,
        workouts=[generated_workouts],
    )

    return plan

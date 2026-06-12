from domain.workout import Workout, Intensity
from domain.training_plan import TrainingPlan
from domain.templates import (
    BEGINNER_MICROCYCLE,
    BEGINNER_VOLUME_DISTRIBUTION,
    INTENSITY_MAPPING,
)

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

    # 2. Empty list to hold the generated workouts
    generated_workouts = []

    current_week_mileage = starting_mileage

    # 3. Loop
    for week in range(total_weeks):

        for day in BEGINNER_MICROCYCLE:
            days_passed = (week * 7) + day
            scheduled_date = today + timedelta(days=days_passed)

            run_type = BEGINNER_MICROCYCLE[day]
            daily_weight = BEGINNER_VOLUME_DISTRIBUTION[day]
            daily_intensity = INTENSITY_MAPPING[run_type]

            daily_distance = round(current_week_mileage * daily_weight, 2)

            create_workout = Workout(
                type=run_type,
                distance=daily_distance,
                intensity=daily_intensity,
                scheduled_date=scheduled_date,
            )

            generated_workouts.append(create_workout)

        current_week_mileage = current_week_mileage * 1.10

    # Create a training plan
    plan = TrainingPlan(
        race_date=race_date,
        goal_time=goal_time,
        starting_mileage=starting_mileage,
        workouts=[generated_workouts],
    )

    return plan

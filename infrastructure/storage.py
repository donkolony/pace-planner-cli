from domain.training_plan import TrainingPlan
from datetime import timedelta


def serialize_training_plan(plan: TrainingPlan) -> dict:

    # The Workouts
    serialize_workouts = []

    for workout in plan.workouts:

        # Build the Workout Dictionary
        workout_dict = {
            "type": workout.type.value,
            "distance": workout.distance,
            "intensity": workout.intensity.name,
            "date": workout.scheduled_date.strftime("%m-%d-%Y"),
        }

        serialize_workouts.append(workout_dict)

    # Build the Master Dictionary
    master_plan_dict = {
        "race_date": plan.race_date.strftime("%m-%d-%Y"),
        "starting_mileage": plan.starting_mileage,
        "goal_time": str(plan.goal_time),
        "workouts": serialize_workouts,
    }

    return master_plan_dict

import json
from datetime import datetime, timedelta

from domain.training_plan import TrainingPlan
from domain.workout import Intensity, RunTypes, Workout


def serialize_training_plan(plan: TrainingPlan) -> dict:

    # The Workouts
    serialize_workouts = []

    for workout in plan.workouts:
        # Build the Workout Dictionary
        workout_dict = {
            "type": workout.type.value,
            "distance": workout.distance,
            "intensity": workout.intensity.value,
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


def save_plan_to_local_storage(
    plan: TrainingPlan, file_path: str = "paceplanner_data.json"
):

    master_plan = serialize_training_plan(plan)

    with open(file_path, "w") as f:  
        json.dump(master_plan, f, indent=4)


def load_plan_from_local_storage(
    file_path: str = "paceplanner_data.json",
) -> TrainingPlan:

    with open(file_path, "r") as f:
        raw_data = json.load(f)

        race_date = datetime.strptime(raw_data.get("race_date"), "%m-%d-%Y")
        starting_mileage = raw_data.get("starting_mileage")

        # Grab the string and split it into a list of 3 parts
        goal_time_parts = raw_data.get("goal_time").split(":")

        # Unpack the list directly into three name variables
        h, m, s = goal_time_parts

        workouts = raw_data.get("workouts")

        parsed_workouts = []

        for workout in workouts:
            type = workout.get("type")
            distance = workout.get("distance")
            intensity = workout.get("intensity")
            date = workout.get("date")

            parsed_workout = Workout(
                type=RunTypes(type),
                distance=distance,
                intensity=Intensity(intensity),
                scheduled_date=datetime.strptime(date, "%m-%d-%Y"),
            )

            parsed_workouts.append(parsed_workout)

        reconstructed_plan = TrainingPlan(
            race_date,
            timedelta(hours=int(h), minutes=int(m), seconds=int(s)),
            starting_mileage,
            parsed_workouts,
        )

        return reconstructed_plan

from datetime import datetime, timedelta
from typing import Annotated

import typer

from infrastructure.storage import load_plan_from_local_storage
from services.plan_generator import generate_training_plan

app = typer.Typer()


@app.command()
def init(
    race_date: Annotated[datetime, typer.Option(prompt="Enter your race date ")],
    goal_hours: Annotated[int, typer.Option(prompt="Enter the hour ")],
    goal_minutes: Annotated[int, typer.Option(prompt="Enter the minutes")],
    current_weekly_mileage: Annotated[
        float, typer.Option(prompt="Enter your current weekly mileage ")
    ],
):

    plan = generate_training_plan(
        race_date,
        timedelta(hours=goal_hours, minutes=goal_minutes),
        current_weekly_mileage,
    )

    # save_plan_to_local_storage(plan)

    print("Plan created successfully :)")


@app.command()
def today():

    now = datetime.now()

    reconstructed_plan = load_plan_from_local_storage()

    # Loop through workuts and find matching date
    for workout in reconstructed_plan.workouts:
        if now.date() == workout.scheduled_date.date():
            print(
                f"🏃 Today's Workout: {workout.distance}km ({workout.type.value} - {workout.intensity.name})"
            )
            return

    print("Rest day...rest Bafo!")


if __name__ == "__main__":
    app()

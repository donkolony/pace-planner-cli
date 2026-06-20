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

    today = datetime.now()

    reconstructed_plan = load_plan_from_local_storage()

    # Loop through workuts and find matching date
    for workout in reconstructed_plan.workouts:
        if today.date() == workout.scheduled_date.date():
            print(
                f"🏃 Today's Workout: {workout.distance}km ({workout.type.value} - {workout.intensity.name})"
            )
            return

    print("Rest day...rest Bafo!")


@app.command()
def week():

    # Get current date and format it
    today = datetime.now().date()
    end_of_week = today + timedelta(days=7)

    reconstructed_plan = load_plan_from_local_storage()

    print("\n📅 Your Schedule for the next 7 Days:")

    for workout in reconstructed_plan.workouts:
        if today <= workout.scheduled_date.date() <= end_of_week:
            print(
                f"{workout.scheduled_date.date().strftime('%A, %b, %d')}: Workout: {workout.distance}km ({workout.type.value} - {workout.intensity.name})"
            )


if __name__ == "__main__":
    app()

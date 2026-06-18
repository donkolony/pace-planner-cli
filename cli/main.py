from typing import Annotated

from datetime import datetime, timedelta

from services.plan_generator import generate_training_plan
from infrastructure.storage import save_plan_to_local_storage


import typer

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

    save_plan_to_local_storage(plan)

    print("Plan created successfully :)")


if __name__ == "__main__":
    app()

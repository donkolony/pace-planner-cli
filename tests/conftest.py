import pytest
from datetime import datetime, timedelta
from domain.workout import Workout, RunTypes, Intensity
from domain.training_plan import TrainingPlan

# ── Datetime helpers ──────────────────────────────────────────────────────────


@pytest.fixture
def race_date() -> datetime:
    """A future race date (10 weeks out)."""
    return datetime(2026, 10, 15)


@pytest.fixture
def goal_time() -> timedelta:
    """A typical marathon goal time: 4 h 30 m."""
    return timedelta(hours=4, minutes=30)


@pytest.fixture
def starting_mileage() -> float:
    return 20.0


# ── Domain object fixtures ────────────────────────────────────────────────────


@pytest.fixture
def easy_workout() -> Workout:
    return Workout(
        type=RunTypes.EASY,
        distance=5.0,
        intensity=Intensity.ZONE_2,
        scheduled_date=datetime(2026, 6, 10),
    )


@pytest.fixture
def tempo_workout() -> Workout:
    return Workout(
        type=RunTypes.TEMPO,
        distance=8.0,
        intensity=Intensity.ZONE_4,
        scheduled_date=datetime(2026, 6, 11),
    )


@pytest.fixture
def long_run_workout() -> Workout:
    return Workout(
        type=RunTypes.LONG_RUN,
        distance=20.0,
        intensity=Intensity.ZONE_2,
        scheduled_date=datetime(2026, 6, 14),
    )


@pytest.fixture
def rest_workout() -> Workout:
    return Workout(
        type=RunTypes.REST,
        distance=0.0,
        intensity=Intensity.ZONE_1,
        scheduled_date=datetime(2026, 6, 9),
    )


@pytest.fixture
def sample_plan(
    race_date, goal_time, starting_mileage, easy_workout, tempo_workout
) -> TrainingPlan:
    return TrainingPlan(
        race_date=race_date,
        goal_time=goal_time,
        starting_mileage=starting_mileage,
        workouts=[easy_workout, tempo_workout],
    )

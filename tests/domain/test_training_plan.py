import pytest
from datetime import datetime, timedelta
from domain.training_plan import TrainingPlan
from domain.workout import Workout, RunTypes, Intensity

# ─────────────────────────────────────────────
# Construction & field storage
# ─────────────────────────────────────────────


class TestTrainingPlanConstruction:

    def test_fields_stored_correctly(self, race_date, goal_time, starting_mileage):
        plan = TrainingPlan(
            race_date=race_date,
            goal_time=goal_time,
            starting_mileage=starting_mileage,
        )
        assert plan.race_date == race_date
        assert plan.goal_time == goal_time
        assert plan.starting_mileage == starting_mileage

    def test_default_workouts_is_empty_list(self, race_date, goal_time):
        plan = TrainingPlan(
            race_date=race_date, goal_time=goal_time, starting_mileage=10.0
        )
        assert plan.workouts == []

    def test_workouts_default_is_mutable_list(self, race_date, goal_time):
        plan = TrainingPlan(
            race_date=race_date, goal_time=goal_time, starting_mileage=10.0
        )
        assert isinstance(plan.workouts, list)

    def test_mutable_default_isolation(self, race_date, goal_time):
        """Two plans must NOT share the same workouts list (dataclass field default_factory)."""
        plan_a = TrainingPlan(
            race_date=race_date, goal_time=goal_time, starting_mileage=10.0
        )
        plan_b = TrainingPlan(
            race_date=race_date, goal_time=goal_time, starting_mileage=10.0
        )
        plan_a.workouts.append(
            Workout(RunTypes.EASY, 5.0, Intensity.ZONE_2, datetime(2026, 7, 1))
        )
        assert (
            len(plan_b.workouts) == 0
        ), "plan_b.workouts should not be polluted by plan_a"

    def test_explicit_workouts_list_stored(
        self, race_date, goal_time, easy_workout, tempo_workout
    ):
        plan = TrainingPlan(
            race_date=race_date,
            goal_time=goal_time,
            starting_mileage=20.0,
            workouts=[easy_workout, tempo_workout],
        )
        assert len(plan.workouts) == 2
        assert plan.workouts[0] is easy_workout
        assert plan.workouts[1] is tempo_workout


# ─────────────────────────────────────────────
# Field type contracts
# ─────────────────────────────────────────────


class TestTrainingPlanFieldTypes:

    def test_race_date_is_datetime(self, sample_plan):
        assert isinstance(sample_plan.race_date, datetime)

    def test_goal_time_is_timedelta(self, sample_plan):
        assert isinstance(sample_plan.goal_time, timedelta)

    def test_starting_mileage_value(self, sample_plan):
        assert sample_plan.starting_mileage == 20.0

    def test_workouts_is_list_of_workouts(self, sample_plan):
        assert isinstance(sample_plan.workouts, list)
        for w in sample_plan.workouts:
            assert isinstance(w, Workout)


# ─────────────────────────────────────────────
# Workout list manipulation
# ─────────────────────────────────────────────


class TestTrainingPlanWorkoutList:

    def test_append_workout_to_plan(self, sample_plan, long_run_workout):
        initial_count = len(sample_plan.workouts)
        sample_plan.workouts.append(long_run_workout)
        assert len(sample_plan.workouts) == initial_count + 1
        assert sample_plan.workouts[-1] is long_run_workout

    def test_remove_workout_from_plan(self, sample_plan, easy_workout):
        sample_plan.workouts.remove(easy_workout)
        assert easy_workout not in sample_plan.workouts

    def test_workout_ordering_preserved(self, race_date, goal_time):
        dates = [datetime(2026, 7, d) for d in range(1, 6)]
        workouts = [
            Workout(RunTypes.EASY, float(d), Intensity.ZONE_2, dates[i])
            for i, d in enumerate(range(1, 6))
        ]
        plan = TrainingPlan(
            race_date=race_date,
            goal_time=goal_time,
            starting_mileage=15.0,
            workouts=workouts,
        )
        for i, w in enumerate(plan.workouts):
            assert w.scheduled_date == dates[i]

    def test_plan_with_only_rest_days(self, race_date, goal_time):
        rest_days = [
            Workout(RunTypes.REST, 0.0, Intensity.ZONE_1, datetime(2026, 7, d))
            for d in range(1, 8)
        ]
        plan = TrainingPlan(
            race_date=race_date,
            goal_time=goal_time,
            starting_mileage=0.0,
            workouts=rest_days,
        )
        assert all(w.type is RunTypes.REST for w in plan.workouts)


# ─────────────────────────────────────────────
# Goal time edge cases
# ─────────────────────────────────────────────


class TestTrainingPlanGoalTime:

    def test_sub_3_hour_goal(self, race_date):
        plan = TrainingPlan(
            race_date=race_date,
            goal_time=timedelta(hours=2, minutes=59, seconds=59),
            starting_mileage=60.0,
        )
        assert plan.goal_time < timedelta(hours=3)

    def test_goal_time_in_seconds_accessible(self, race_date):
        goal = timedelta(hours=4, minutes=30)
        plan = TrainingPlan(race_date=race_date, goal_time=goal, starting_mileage=20.0)
        assert plan.goal_time.total_seconds() == 16200.0

    def test_equality_of_identical_plans(self, race_date, goal_time, easy_workout):
        plan_a = TrainingPlan(race_date, goal_time, 20.0, [easy_workout])
        plan_b = TrainingPlan(race_date, goal_time, 20.0, [easy_workout])
        assert plan_a == plan_b

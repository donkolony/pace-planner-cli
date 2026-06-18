from datetime import datetime, timedelta
from unittest.mock import patch

from services.plan_generator import generate_training_plan
from domain.training_plan import TrainingPlan
from domain.workout import Workout, RunTypes, Intensity
from domain.templates import BEGINNER_MICROCYCLE

# ── Shared constants ──────────────────────────────────────────────────────────

TODAY = datetime(2026, 6, 5, 0, 0, 0)
RACE_2W = TODAY + timedelta(weeks=2)  # 14 days  → 2  full weeks
RACE_10W = TODAY + timedelta(weeks=10)  # 70 days  → 10 full weeks
RACE_13D = TODAY + timedelta(days=13)  # 13 days  → 1  full week  (remainder dropped)
RACE_PAST = TODAY - timedelta(days=1)  # yesterday → 0 weeks

DAYS_PER_WEEK = len(BEGINNER_MICROCYCLE)  # 7


def make_plan(race_date, goal_time=None, starting_mileage=20.0):
    """Helper: call generator with today patched to TODAY."""
    if goal_time is None:
        goal_time = timedelta(hours=4, minutes=30)
    with patch("services.plan_generator.datetime") as mock_dt:
        mock_dt.now.return_value = TODAY
        mock_dt.side_effect = None  # keep timedelta arithmetic working
        return generate_training_plan(race_date, goal_time, starting_mileage)


# ─────────────────────────────────────────────
# Return type & structure
# ─────────────────────────────────────────────


class TestReturnType:

    def test_returns_training_plan_instance(self):
        plan = make_plan(RACE_2W)
        assert isinstance(plan, TrainingPlan)

    def test_workouts_field_is_a_list(self):
        plan = make_plan(RACE_2W)
        assert isinstance(plan.workouts, list)

    def test_every_element_is_a_workout(self):
        plan = make_plan(RACE_10W)
        for w in plan.workouts:
            assert isinstance(w, Workout), f"Expected Workout, got {type(w)}"


# ─────────────────────────────────────────────
# Input propagation
# ─────────────────────────────────────────────


class TestInputPropagation:

    def test_race_date_stored_on_plan(self):
        plan = make_plan(RACE_10W)
        assert plan.race_date == RACE_10W

    def test_goal_time_stored_on_plan(self):
        goal = timedelta(hours=3, minutes=45)
        plan = make_plan(RACE_10W, goal_time=goal)
        assert plan.goal_time == goal

    def test_starting_mileage_stored_on_plan(self):
        plan = make_plan(RACE_10W, starting_mileage=35.5)
        assert plan.starting_mileage == 35.5

    def test_zero_starting_mileage_accepted(self):
        plan = make_plan(RACE_2W, starting_mileage=0.0)
        assert plan.starting_mileage == 0.0

    def test_high_starting_mileage_accepted(self):
        plan = make_plan(RACE_10W, starting_mileage=150.0)
        assert plan.starting_mileage == 150.0


# ─────────────────────────────────────────────
# Workout count — week calculation
# ─────────────────────────────────────────────


class TestWorkoutCount:

    def test_two_week_plan_has_14_workouts(self):
        plan = make_plan(RACE_2W)
        assert len(plan.workouts) == 14

    def test_ten_week_plan_has_70_workouts(self):
        plan = make_plan(RACE_10W)
        assert len(plan.workouts) == 70

    def test_partial_week_remainder_is_dropped(self):
        """13 days = 1 full week + 6 days; only the full week is scheduled."""
        plan = make_plan(RACE_13D)
        assert len(plan.workouts) == 7

    def test_race_in_past_produces_empty_plan(self):
        plan = make_plan(RACE_PAST)
        assert plan.workouts == []

    def test_race_less_than_one_week_away_produces_empty_plan(self):
        near_race = TODAY + timedelta(days=6)
        plan = make_plan(near_race)
        assert plan.workouts == []

    def test_exactly_one_week_produces_7_workouts(self):
        plan = make_plan(TODAY + timedelta(weeks=1))
        assert len(plan.workouts) == 7

    def test_workout_count_scales_linearly_with_weeks(self):
        for weeks in range(1, 6):
            plan = make_plan(TODAY + timedelta(weeks=weeks))
            assert len(plan.workouts) == weeks * DAYS_PER_WEEK


# ─────────────────────────────────────────────
# Scheduled dates
# ─────────────────────────────────────────────


class TestScheduledDates:

    def test_all_scheduled_dates_are_datetime_instances(self):
        plan = make_plan(RACE_2W)
        for w in plan.workouts:
            assert isinstance(w.scheduled_date, datetime)

    def test_first_workout_is_scheduled_on_today(self):
        """Day 0 of week 0: days_passed = 0, so scheduled_date == today."""
        plan = make_plan(RACE_2W)
        assert plan.workouts[0].scheduled_date == TODAY

    def test_second_workout_is_one_day_after_today(self):
        plan = make_plan(RACE_2W)
        assert plan.workouts[1].scheduled_date == TODAY + timedelta(days=1)

    def test_last_workout_is_before_race_date(self):
        plan = make_plan(RACE_10W)
        assert plan.workouts[-1].scheduled_date < RACE_10W

    def test_workouts_are_in_chronological_order(self):
        plan = make_plan(RACE_2W)
        dates = [w.scheduled_date for w in plan.workouts]
        assert dates == sorted(dates)

    def test_no_workout_scheduled_on_or_after_race_date(self):
        plan = make_plan(RACE_10W)
        for w in plan.workouts:
            assert w.scheduled_date < RACE_10W

    def test_second_week_starts_7_days_after_first(self):
        """Week 1 day 0 should be exactly 7 days after week 0 day 0."""
        plan = make_plan(RACE_2W)
        week0_day0 = plan.workouts[0].scheduled_date
        week1_day0 = plan.workouts[DAYS_PER_WEEK].scheduled_date
        assert (week1_day0 - week0_day0) == timedelta(days=7)

    def test_consecutive_workouts_are_one_day_apart(self):
        plan = make_plan(RACE_2W)
        for i in range(1, len(plan.workouts)):
            delta = (
                plan.workouts[i].scheduled_date - plan.workouts[i - 1].scheduled_date
            )
            assert delta == timedelta(days=1)


# ─────────────────────────────────────────────
# Run type sequencing (microcycle pattern)
# ─────────────────────────────────────────────


class TestRunTypeSequencing:

    def test_first_workout_matches_microcycle_day_0(self):
        plan = make_plan(RACE_2W)
        assert plan.workouts[0].type == BEGINNER_MICROCYCLE[0]

    def test_full_week_run_type_sequence_matches_microcycle(self):
        """The first 7 workouts must mirror BEGINNER_MICROCYCLE in order."""
        plan = make_plan(RACE_2W)
        for i, day_key in enumerate(BEGINNER_MICROCYCLE):
            assert plan.workouts[i].type == BEGINNER_MICROCYCLE[day_key], (
                f"Workout {i} (day key {day_key}): "
                f"expected {BEGINNER_MICROCYCLE[day_key]}, got {plan.workouts[i].type}"
            )

    def test_microcycle_pattern_repeats_in_week_2(self):
        """Week 2 workouts must have the same run types as week 1."""
        plan = make_plan(RACE_2W)
        week1 = [w.type for w in plan.workouts[:DAYS_PER_WEEK]]
        week2 = [w.type for w in plan.workouts[DAYS_PER_WEEK:]]
        assert week1 == week2

    def test_all_workout_run_types_are_valid_enum_members(self):
        plan = make_plan(RACE_10W)
        for w in plan.workouts:
            assert isinstance(w.type, RunTypes)

    def test_rest_days_have_correct_position_each_week(self):
        """REST falls on day 0 (Monday) and day 4 (Friday) every week."""
        rest_day_keys = {
            k for k, v in BEGINNER_MICROCYCLE.items() if v is RunTypes.REST
        }
        plan = make_plan(RACE_2W)
        for week in range(2):
            for day_key in rest_day_keys:
                idx = week * DAYS_PER_WEEK + day_key
                assert (
                    plan.workouts[idx].type is RunTypes.REST
                ), f"Week {week} day {day_key} should be REST"

    def test_long_run_falls_on_day_5_each_week(self):
        plan = make_plan(RACE_2W)
        for week in range(2):
            idx = week * DAYS_PER_WEEK + 5  # day 5 = Saturday
            assert plan.workouts[idx].type is RunTypes.LONG_RUN

    def test_tempo_run_falls_on_day_2_each_week(self):
        plan = make_plan(RACE_2W)
        for week in range(2):
            idx = week * DAYS_PER_WEEK + 2  # day 2 = Wednesday
            assert plan.workouts[idx].type is RunTypes.TEMPO


# ─────────────────────────────────────────────
# Workout field values (current fixed stub values)
# ─────────────────────────────────────────────


class TestWorkoutFieldValues:

    def test_all_workouts_have_distance_5(self):
        """Distance is hard-coded to 5.0 until dynamic logic is implemented."""
        plan = make_plan(RACE_2W)
        for w in plan.workouts:
            assert w.distance == 5.0

    def test_all_workouts_have_zone_2_intensity(self):
        """Intensity is hard-coded to ZONE_2 until dynamic logic is implemented."""
        plan = make_plan(RACE_2W)
        for w in plan.workouts:
            assert w.intensity is Intensity.ZONE_2

    def test_distance_is_non_negative(self):
        plan = make_plan(RACE_10W)
        for w in plan.workouts:
            assert w.distance >= 0


# ─────────────────────────────────────────────
# State isolation between calls
# ─────────────────────────────────────────────


class TestStateIsolation:

    def test_two_calls_return_independent_workout_lists(self):
        plan_a = make_plan(RACE_2W)
        plan_b = make_plan(RACE_2W)
        plan_a.workouts.clear()
        assert len(plan_b.workouts) == 14, "plan_b was polluted by mutating plan_a"

    def test_longer_race_produces_more_workouts_than_shorter(self):
        short_plan = make_plan(RACE_2W)
        long_plan = make_plan(RACE_10W)
        assert len(long_plan.workouts) > len(short_plan.workouts)

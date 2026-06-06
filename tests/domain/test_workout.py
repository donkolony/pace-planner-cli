import pytest
from datetime import datetime
from domain.workout import Workout, RunTypes, Intensity

# ─────────────────────────────────────────────
# RunTypes enum
# ─────────────────────────────────────────────


class TestRunTypes:

    def test_all_expected_members_present(self):
        names = {m.name for m in RunTypes}
        assert names == {"EASY", "TEMPO", "LONG_RUN", "INTERVAL", "REST"}

    def test_string_values_are_human_readable(self):
        assert RunTypes.EASY.value == "easy"
        assert RunTypes.TEMPO.value == "tempo"
        assert RunTypes.LONG_RUN.value == "long run"
        assert RunTypes.INTERVAL.value == "interval"
        assert RunTypes.REST.value == "rest"

    def test_members_are_unique(self):
        values = [m.value for m in RunTypes]
        assert len(values) == len(set(values)), "Duplicate enum values detected"

    def test_lookup_by_value(self):
        assert RunTypes("easy") is RunTypes.EASY
        assert RunTypes("long run") is RunTypes.LONG_RUN

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            RunTypes("sprint")


# ─────────────────────────────────────────────
# Intensity enum
# ─────────────────────────────────────────────


class TestIntensity:

    def test_all_five_zones_present(self):
        names = {m.name for m in Intensity}
        assert names == {"ZONE_1", "ZONE_2", "ZONE_3", "ZONE_4", "ZONE_5"}

    def test_zone_string_values(self):
        assert Intensity.ZONE_1.value == "recovery"
        assert Intensity.ZONE_2.value == "easy"
        assert Intensity.ZONE_3.value == "moderate"
        assert Intensity.ZONE_4.value == "tempo"
        assert Intensity.ZONE_5.value == "maximum"

    def test_members_are_unique(self):
        values = [m.value for m in Intensity]
        assert len(values) == len(set(values)), "Duplicate enum values detected"

    def test_lookup_by_value(self):
        assert Intensity("tempo") is Intensity.ZONE_4
        assert Intensity("recovery") is Intensity.ZONE_1

    def test_invalid_value_raises(self):
        with pytest.raises(ValueError):
            Intensity("super hard")


# ─────────────────────────────────────────────
# Workout dataclass
# ─────────────────────────────────────────────


class TestWorkoutConstruction:

    def test_explicit_fields_stored_correctly(self):
        date = datetime(2026, 8, 1)
        w = Workout(
            type=RunTypes.TEMPO,
            distance=10.0,
            intensity=Intensity.ZONE_4,
            scheduled_date=date,
        )
        assert w.type is RunTypes.TEMPO
        assert w.distance == 10.0
        assert w.intensity is Intensity.ZONE_4
        assert w.scheduled_date == date

    def test_default_scheduled_date_is_datetime(self):
        """Omitting scheduled_date should still produce a datetime instance."""
        w = Workout(type=RunTypes.EASY, distance=5.0, intensity=Intensity.ZONE_2)
        assert isinstance(w.scheduled_date, datetime)

    def test_rest_workout_zero_distance(self, rest_workout):
        assert rest_workout.distance == 0.0
        assert rest_workout.type is RunTypes.REST

    def test_long_run_distance(self, long_run_workout):
        assert long_run_workout.distance == 20.0
        assert long_run_workout.type is RunTypes.LONG_RUN


class TestWorkoutFieldTypes:

    def test_type_field_accepts_only_run_types_enum(self):
        """Ensure type is stored as the enum member, not a plain string."""
        w = Workout(type=RunTypes.EASY, distance=3.0, intensity=Intensity.ZONE_2)
        assert isinstance(w.type, RunTypes)

    def test_intensity_field_accepts_only_intensity_enum(self):
        w = Workout(type=RunTypes.EASY, distance=3.0, intensity=Intensity.ZONE_2)
        assert isinstance(w.intensity, Intensity)

    def test_distance_stored_as_float(self):
        w = Workout(type=RunTypes.EASY, distance=5, intensity=Intensity.ZONE_2)
        # int input is acceptable; the value should compare correctly
        assert w.distance == 5

    def test_large_distance_stored_correctly(self):
        w = Workout(type=RunTypes.LONG_RUN, distance=42.195, intensity=Intensity.ZONE_2)
        assert pytest.approx(w.distance) == 42.195


class TestWorkoutEquality:

    def test_identical_workouts_are_equal(self):
        date = datetime(2026, 9, 1)
        w1 = Workout(RunTypes.EASY, 5.0, Intensity.ZONE_2, date)
        w2 = Workout(RunTypes.EASY, 5.0, Intensity.ZONE_2, date)
        assert w1 == w2

    def test_different_type_makes_workouts_unequal(self):
        date = datetime(2026, 9, 1)
        w1 = Workout(RunTypes.EASY, 5.0, Intensity.ZONE_2, date)
        w2 = Workout(RunTypes.TEMPO, 5.0, Intensity.ZONE_2, date)
        assert w1 != w2

    def test_different_distance_makes_workouts_unequal(self):
        date = datetime(2026, 9, 1)
        w1 = Workout(RunTypes.EASY, 5.0, Intensity.ZONE_2, date)
        w2 = Workout(RunTypes.EASY, 6.0, Intensity.ZONE_2, date)
        assert w1 != w2

import pytest
from domain.workout import RunTypes
from domain.templates import BEGINNER_MICROCYCLE


class TestBeginnerMicrocycleStructure:

    def test_covers_all_seven_days(self):
        assert set(BEGINNER_MICROCYCLE.keys()) == {0, 1, 2, 3, 4, 5, 6}

    def test_keys_are_integers(self):
        for key in BEGINNER_MICROCYCLE:
            assert isinstance(key, int), f"Key {key!r} is not an int"

    def test_values_are_run_types(self):
        for day, run_type in BEGINNER_MICROCYCLE.items():
            assert isinstance(
                run_type, RunTypes
            ), f"Day {day} has value {run_type!r}, expected RunTypes member"

    def test_no_duplicate_days(self):
        keys = list(BEGINNER_MICROCYCLE.keys())
        assert len(keys) == len(set(keys))


class TestBeginnerMicrocycleDayAssignments:
    """
    Validate the intended weekly schedule:
      Mon(0)=REST, Tue(1)=EASY, Wed(2)=TEMPO, Thu(3)=EASY,
      Fri(4)=REST, Sat(5)=LONG_RUN, Sun(6)=EASY
    """

    def test_monday_is_rest(self):
        assert BEGINNER_MICROCYCLE[0] is RunTypes.REST

    def test_tuesday_is_easy(self):
        assert BEGINNER_MICROCYCLE[1] is RunTypes.EASY

    def test_wednesday_is_tempo(self):
        assert BEGINNER_MICROCYCLE[2] is RunTypes.TEMPO

    def test_thursday_is_easy(self):
        assert BEGINNER_MICROCYCLE[3] is RunTypes.EASY

    def test_friday_is_rest(self):
        assert BEGINNER_MICROCYCLE[4] is RunTypes.REST

    def test_saturday_is_long_run(self):
        assert BEGINNER_MICROCYCLE[5] is RunTypes.LONG_RUN

    def test_sunday_is_easy(self):
        assert BEGINNER_MICROCYCLE[6] is RunTypes.EASY


class TestBeginnerMicrocycleDistribution:

    def test_exactly_two_rest_days(self):
        rest_days = [d for d, t in BEGINNER_MICROCYCLE.items() if t is RunTypes.REST]
        assert (
            len(rest_days) == 2
        ), f"Expected 2 rest days, got {len(rest_days)}: {rest_days}"

    def test_exactly_one_long_run(self):
        long_runs = [
            d for d, t in BEGINNER_MICROCYCLE.items() if t is RunTypes.LONG_RUN
        ]
        assert len(long_runs) == 1

    def test_exactly_one_tempo_run(self):
        tempo_runs = [d for d, t in BEGINNER_MICROCYCLE.items() if t is RunTypes.TEMPO]
        assert len(tempo_runs) == 1

    def test_exactly_three_easy_runs(self):
        easy_runs = [d for d, t in BEGINNER_MICROCYCLE.items() if t is RunTypes.EASY]
        assert len(easy_runs) == 3

    def test_no_interval_days_in_beginner_plan(self):
        """Interval runs are not appropriate for beginner templates."""
        interval_days = [
            d for d, t in BEGINNER_MICROCYCLE.items() if t is RunTypes.INTERVAL
        ]
        assert interval_days == [], f"Unexpected INTERVAL days: {interval_days}"

    def test_hard_days_are_not_adjacent(self):
        """
        Tempo (Wed=2) and Long Run (Sat=5) should not be on consecutive days.
        Verifies the template follows basic training load principles.
        """
        hard_days = sorted(
            d
            for d, t in BEGINNER_MICROCYCLE.items()
            if t in (RunTypes.TEMPO, RunTypes.LONG_RUN)
        )
        for i in range(len(hard_days) - 1):
            gap = hard_days[i + 1] - hard_days[i]
            assert gap > 1, (
                f"Hard days {hard_days[i]} and {hard_days[i+1]} are adjacent — "
                "insufficient recovery"
            )

from domain.workout import RunTypes

# 0 = Monday, 6 = Sunday
BEGINNER_MICROCYCLE = {
    0: RunTypes.REST,  # Monday: Rest
    1: RunTypes.EASY,  # Tuesday: Easy Run
    2: RunTypes.TEMPO,  # Wednesday: Tempo Run
    3: RunTypes.EASY,  # Thursday: Easy Run
    4: RunTypes.REST,  # Friday: Rest
    5: RunTypes.LONG_RUN,  # Saturday: Long Run
    6: RunTypes.EASY,  # Sunday: Recovery Run (Easy)
}

# TODO: Implement advanced microcylce templates in future

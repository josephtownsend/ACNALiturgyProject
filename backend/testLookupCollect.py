from datetime import date
from calendarEngine import getLiturgicalDayDetailed
from lookupCollect import lookupCollect

# --- Test Cases ---

def testLookup(givenDate):
    calendarInfo = getLiturgicalDayDetailed(givenDate)
    result = lookupCollect(givenDate, calendarInfo)
    print(f"\nDate: {givenDate.isoformat()}")
    print(f"Liturgical Label: {calendarInfo['feastOrSeasonName']}")
    print(f"Season: {calendarInfo['season']}")
    print(f"Collect (excerpt): {result['collect'][:80]}...")
    print(f"Preface Key: {result['prefaceKey']}")

# --- Run Tests ---

testDates = [
    # Major Feasts
    date(2025, 12, 25),  # Christmas
    date(2026, 1, 6),    # Epiphany
    date(2026, 3, 29),   # Palm Sunday
    date(2026, 4, 5),    # Easter Day
    date(2026, 5, 14),   # Ascension Day
    date(2026, 5, 24),   # Pentecost
    date(2026, 5, 31),   # Trinity Sunday
    date(2025, 11, 2),   # All Saints (Sunday move)

    # Seasonal Sundays
    date(2025, 11, 30),  # 1st Sunday in Advent
    date(2026, 2, 15),   # 2nd Sunday before Lent (should still be after Epiphany)
    date(2026, 2, 22),   # Last Sunday after Epiphany
    date(2026, 3, 1),    # 1st Sunday in Lent
    date(2026, 4, 19),   # 2nd Sunday in Eastertide
    date(2026, 6, 14),   # 1st Sunday after Trinity (Proper 6 time)

    # Ember Days
    date(2026, 2, 25),   # Ember Wednesday (Lent)
    date(2026, 5, 27),   # Ember Wednesday after Pentecost
    date(2025, 9, 17),   # Ember Wednesday (after Holy Cross)

    # Rogation Days
    date(2026, 5, 11),   # Rogation Monday
    date(2026, 5, 12),   # Rogation Tuesday
    date(2026, 5, 13),   # Rogation Wednesday

    # Weekdays (Ordinary)
    date(2026, 1, 8),    # Ordinary Thursday after Epiphany (inherits Epiphanytide)
    date(2026, 6, 18),   # Thursday after 2nd Sunday after Trinity (Proper 7)

    # Fixed Saints
    date(2026, 6, 24),   # Nativity of St. John the Baptist
    date(2026, 6, 29),   # St. Peter and St. Paul
    date(2026, 8, 6),    # Transfiguration
    date(2026, 9, 29),   # Holy Michael and All Angels

    # Commons (if needed later)
    # Assume we simulate a custom labeling triggering a Common
    # date(2026, 7, 22),  # (St Mary Magdalene uses dedicated collect already)
]

for d in testDates:
    testLookup(d)

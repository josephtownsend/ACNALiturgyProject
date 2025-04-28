# testCalendarEngine.py
from datetime import date
import calendarEngine

print(calendarEngine.getLiturgicalDayDetailed(date(2026, 4, 5)))
print(calendarEngine.getLiturgicalDayDetailed(date(2025, 11, 2)))
print(calendarEngine.getLiturgicalDayDetailed(date(2025, 2, 2)))

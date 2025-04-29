# properUtils.py

# List of Proper date ranges (month and day only)
properDateRanges = [
    {"key": "proper1", "startMonth": 5, "startDay": 8, "endMonth": 5, "endDay": 14},
    {"key": "proper2", "startMonth": 5, "startDay": 15, "endMonth": 5, "endDay": 21},
    {"key": "proper3", "startMonth": 5, "startDay": 22, "endMonth": 5, "endDay": 28},
    {"key": "proper4", "startMonth": 5, "startDay": 29, "endMonth": 6, "endDay": 4},
    {"key": "proper5", "startMonth": 6, "startDay": 5, "endMonth": 6, "endDay": 11},
    {"key": "proper6", "startMonth": 6, "startDay": 12, "endMonth": 6, "endDay": 18},
    {"key": "proper7", "startMonth": 6, "startDay": 19, "endMonth": 6, "endDay": 25},
    {"key": "proper8", "startMonth": 6, "startDay": 26, "endMonth": 7, "endDay": 2},
    {"key": "proper9", "startMonth": 7, "startDay": 3, "endMonth": 7, "endDay": 9},
    {"key": "proper10", "startMonth": 7, "startDay": 10, "endMonth": 7, "endDay": 16},
    {"key": "proper11", "startMonth": 7, "startDay": 17, "endMonth": 7, "endDay": 23},
    {"key": "proper12", "startMonth": 7, "startDay": 24, "endMonth": 7, "endDay": 30},
    {"key": "proper13", "startMonth": 7, "startDay": 31, "endMonth": 8, "endDay": 6},
    {"key": "proper14", "startMonth": 8, "startDay": 7, "endMonth": 8, "endDay": 13},
    {"key": "proper15", "startMonth": 8, "startDay": 14, "endMonth": 8, "endDay": 20},
    {"key": "proper16", "startMonth": 8, "startDay": 21, "endMonth": 8, "endDay": 27},
    {"key": "proper17", "startMonth": 8, "startDay": 28, "endMonth": 9, "endDay": 3},
    {"key": "proper18", "startMonth": 9, "startDay": 4, "endMonth": 9, "endDay": 10},
    {"key": "proper19", "startMonth": 9, "startDay": 11, "endMonth": 9, "endDay": 17},
    {"key": "proper20", "startMonth": 9, "startDay": 18, "endMonth": 9, "endDay": 24},
    {"key": "proper21", "startMonth": 9, "startDay": 25, "endMonth": 10, "endDay": 1},
    {"key": "proper22", "startMonth": 10, "startDay": 2, "endMonth": 10, "endDay": 8},
    {"key": "proper23", "startMonth": 10, "startDay": 9, "endMonth": 10, "endDay": 15},
    {"key": "proper24", "startMonth": 10, "startDay": 16, "endMonth": 10, "endDay": 22},
    {"key": "proper25", "startMonth": 10, "startDay": 23, "endMonth": 10, "endDay": 29},
    {"key": "proper26", "startMonth": 10, "startDay": 30, "endMonth": 11, "endDay": 5},
    {"key": "proper27", "startMonth": 11, "startDay": 6, "endMonth": 11, "endDay": 12},
    {"key": "proper28", "startMonth": 11, "startDay": 13, "endMonth": 11, "endDay": 19},
    {"key": "proper29", "startMonth": 11, "startDay": 20, "endMonth": 11, "endDay": 26}
]

def matchProper(givenDate):
    """
    Determine which Proper a given date falls into based on month and day ranges.
    
    Args:
        givenDate (datetime.date): The date to check.

    Returns:
        str: The key of the Proper (e.g., 'proper6'), or None if not found.
    """
    month = givenDate.month
    day = givenDate.day
    current = (month, day)

    for proper in properDateRanges:
        start = (proper['startMonth'], proper['startDay'])
        end = (proper['endMonth'], proper['endDay'])

        if start <= current <= end:
            return proper['key']

    return None

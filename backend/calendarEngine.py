from datetime import date, timedelta

# --- Helper Functions ---

def easterDate(year):
    """Computes Easter Sunday date using Anonymous Gregorian algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = 1 + (h + l - 7 * m + 114) % 31
    return date(year, month, day)

def firstSundayOfAdvent(year):
    christmas = date(year, 12, 25)
    daysToPreviousSunday = (christmas.weekday() + 1) % 7
    return christmas - timedelta(days=daysToPreviousSunday + 21)

def ashWednesday(easter):
    return easter - timedelta(days=46)

def pentecost(easter):
    return easter + timedelta(days=49)

def ascension(easter):
    return easter + timedelta(days=39)

def trinitySunday(pentecostDate):
    return pentecostDate + timedelta(days=7)

def weekdayName(d):
    return d.strftime('%A')

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

# --- Calendar Engine ---

def getLiturgicalDayDetailed(givenDate):
    year = givenDate.year
    
    adventStart = firstSundayOfAdvent(year)
    if givenDate < adventStart:
        year -= 1
        adventStart = firstSundayOfAdvent(year)

    christmas = date(year, 12, 25)
    epiphany = date(year + 1, 1, 6)
    easter = easterDate(year + 1)
    ashWed = ashWednesday(easter)
    pentecostDate = pentecost(easter)
    ascensionDate = ascension(easter)
    trinitySundayDate = trinitySunday(pentecostDate)
    nextAdventStart = firstSundayOfAdvent(year + 1)

    fixedFeasts = {
    date(year, 12, 25): "Christmas",
    date(year + 1, 1, 1): "The Circumcision and Holy Name",
    date(year + 1, 1, 6): "Epiphany",
    date(year + 1, 1, 18): "Confession of St. Peter",
    date(year + 1, 1, 25): "Conversion of St. Paul",
    date(year + 1, 2, 2): "Presentation of Christ in the Temple",
    date(year + 1, 2, 24): "St. Matthias's Day",
    date(year + 1, 3, 19): "St. Joseph's Day",
    date(year + 1, 3, 25): "Annunciation",
    date(year + 1, 4, 25): "St. Mark's Day",
    date(year + 1, 5, 1): "St. Philip and St. James's Day",
    date(year + 1, 5, 31): "Visitation",
    date(year + 1, 6, 11): "St. Barnabas's Day",
    date(year + 1, 6, 24): "Nativity of John the Baptist",
    date(year + 1, 6, 29): "St. Peter and St. Paul's Day",
    date(year + 1, 7, 22): "St. Mary Magdalene",
    date(year + 1, 7, 25): "St. James's Day",
    date(year + 1, 8, 6): "Transfiguration",
    date(year + 1, 8, 15): "The Virgin Mary",
    date(year + 1, 8, 24): "St. Bartholomew's Day",
    date(year + 1, 9, 14): "Holy Cross Day",
    date(year + 1, 9, 21): "St. Matthew's Day",
    date(year + 1, 9, 29): "Holy Michael and All Angels",
    date(year + 1, 10, 18): "St. Luke's Day",
    date(year + 1, 10, 23): "James of Jerusalem",
    date(year + 1, 10, 28): "St. Simon and St. Jude",
    date(year + 1, 11, 1): "All Saints' Day",
    date(year + 1, 11, 30): "St. Andrew's Day",
    date(year + 1, 12, 21): "St. Thomas's Day",
    date(year + 1, 12, 26): "St. Stephen's Day",
    date(year + 1, 12, 27): "St. John's Day",
    date(year + 1, 12, 28): "Holy Innocents",
}

    movableFeasts = {
        ashWed: ("Ash Wednesday", "Lent"),
        easter - timedelta(days=7): ("Palm Sunday", "Lent"),
        easter: ("Easter", "Eastertide"),
        ascensionDate: ("Ascension", "Eastertide"),
        pentecostDate: ("Pentecost", "Pentecost"),
        trinitySundayDate: ("Trinity Sunday", "Trinitytide"),
    }

    # 1. Movable Feasts
    if givenDate in movableFeasts:
        feast, season = movableFeasts[givenDate]
        return buildOutput(givenDate, feast, season, None)

    # 2. Fixed Feasts
    if givenDate in fixedFeasts:
        feastName = fixedFeasts[givenDate]
        season = getSeason(givenDate, adventStart, christmas, epiphany, ashWed, easter, pentecostDate, trinitySundayDate)
        return buildOutput(givenDate, feastName, season, None)


    # 3. Sundays
    if givenDate.weekday() == 6:  # Sunday
        if adventStart <= givenDate < christmas:
            weekNum = (givenDate - adventStart).days // 7 + 1
            return buildOutput(givenDate, f"{ordinal(weekNum)} Sunday in Advent", "Advent", weekNum)
        elif christmas <= givenDate < epiphany:
            return buildOutput(givenDate, "First Sunday after Christmas", "Christmastide", 1)
        elif epiphany <= givenDate < ashWed:
            weekNum = (givenDate - epiphany).days // 7 + 1
            return buildOutput(givenDate, f"{ordinal(weekNum)} Sunday after Epiphany", "Epiphanytide", weekNum)
        elif ashWed <= givenDate < easter:
            weekNum = (givenDate - ashWed).days // 7 + 1
            return buildOutput(givenDate, f"{ordinal(weekNum)} Sunday in Lent", "Lent", weekNum)
        elif easter <= givenDate < pentecostDate:
            weekNum = (givenDate - easter).days // 7 + 1
            return buildOutput(givenDate, f"{ordinal(weekNum)} Sunday in Eastertide", "Eastertide", weekNum)
        elif trinitySundayDate <= givenDate < nextAdventStart:
            weekNum = (givenDate - trinitySundayDate).days // 7 + 1
            return buildOutput(givenDate, f"{ordinal(weekNum)} Sunday after Trinity", "Trinitytide", weekNum)

    # 4. Ember Days
    if isEmberDay(givenDate, easter, pentecostDate):
        season = getSeason(givenDate, adventStart, christmas, epiphany, ashWed, easter, pentecostDate, trinitySundayDate)
        return buildOutput(givenDate, f"Ember {weekdayName(givenDate)} in {season}", season, None)

    # 5. Rogation Days
    if isRogationDay(givenDate, ascensionDate):
        return buildOutput(givenDate, f"Rogation {weekdayName(givenDate)}", "Eastertide", None)

    # 6. Ordinary Weekdays
    season = getSeason(givenDate, adventStart, christmas, epiphany, ashWed, easter, pentecostDate, trinitySundayDate)
    weekNum = calculateWeekOfSeason(givenDate, adventStart, christmas, epiphany, ashWed, easter, pentecostDate, trinitySundayDate)
    specialPentecost = (pentecostDate < givenDate < trinitySundayDate)

    if specialPentecost:
        label = f"{weekdayName(givenDate)} after Pentecost"
    else:
        label = f"{ordinal(weekNum)} {weekdayName(givenDate)} in {season}"

    return buildOutput(givenDate, label, season, weekNum)

# --- Internal Support Functions ---

def buildOutput(givenDate, label, season, weekNum):
    return {
        "date": givenDate.isoformat(),
        "feastOrSeasonName": label,
        "season": season,
        "weekOfSeason": weekNum,
        "weekdayName": weekdayName(givenDate),
        "color": getLiturgicalColor(label)
    }

def getSeason(givenDate, adventStart, christmas, epiphany, ashWed, easter, pentecostDate, trinitySundayDate):
    if adventStart <= givenDate < christmas:
        return "Advent"
    elif christmas <= givenDate < epiphany:
        return "Christmastide"
    elif epiphany <= givenDate < ashWed:
        return "Epiphanytide"
    elif ashWed <= givenDate < easter:
        return "Lent"
    elif easter <= givenDate < pentecostDate:
        return "Eastertide"
    elif pentecostDate < givenDate < trinitySundayDate:
        return "Pentecost"
    else:
        return "Trinitytide"

def calculateWeekOfSeason(givenDate, adventStart, christmas, epiphany, ashWed, easter, pentecostDate, trinitySundayDate):
    if adventStart <= givenDate < christmas:
        return (givenDate - adventStart).days // 7 + 1
    elif christmas <= givenDate < epiphany:
        return 1
    elif epiphany <= givenDate < ashWed:
        return (givenDate - epiphany).days // 7 + 1
    elif ashWed <= givenDate < easter:
        return (givenDate - ashWed).days // 7 + 1
    elif easter <= givenDate < pentecostDate:
        return (givenDate - easter).days // 7 + 1
    elif trinitySundayDate <= givenDate:
        return (givenDate - trinitySundayDate).days // 7 + 1
    return None

def isEmberDay(d, easter, pentecostDate):
    emberWeeks = [
        ashWednesday(easter) + timedelta(days=7),
        pentecostDate + timedelta(days=7),
        date(d.year, 9, 14) + timedelta(days=(2 - date(d.year, 9, 14).weekday()) % 7),
        date(d.year, 12, 13) + timedelta(days=(2 - date(d.year, 12, 13).weekday()) % 7)
    ]
    for weekStart in emberWeeks:
        if weekStart <= d < weekStart + timedelta(days=7):
            if d.weekday() in (2, 4, 5):
                return True
    return False

def isRogationDay(d, ascensionDate):
    for delta in range(1, 4):
        if d == ascensionDate - timedelta(days=delta):
            return True
    return False

def getLiturgicalColor(label):
    if any(word in label for word in [
        "Christmas", "Epiphany", "Annunciation", "Presentation", "Circumcision",
        "Conversion of St. Paul", "Confession of St. Peter", "Resurrection", "Ascension",
        "Transfiguration", "Holy Innocents", "Visitation", "Virgin Mary",
        "St. Joseph", "St. John", "St. Stephen", "St. Mary Magdalene", "All Saints' Day",
        "St. James", "St. Philip and St. James", "St. Barnabas", "St. Matthew",
        "St. Peter", "St. Paul", "St. Andrew", "St. Thomas", "St. Luke", "Easter",
    ]):
        return "White"
    elif any(word in label for word in [
        "Good Friday", "Pentecost", "Holy Cross", "Martyr"
    ]):
        return "Red"
    elif "Ember" in label or "Rogation" in label:
        return "Purple"
    elif any(season in label for season in ["Advent", "Lent"]):
        return "Purple"
    else:
        return "Green"


# --- End of Module ---


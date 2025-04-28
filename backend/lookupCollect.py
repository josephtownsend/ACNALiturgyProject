import json
from datetime import timedelta
from datetime import date

# Load collects.json (assume you load it once at app start)
with open('data/collects/collects.json', 'r') as f:
    collectsData = json.load(f)

# Helper: create quick lookup by key
collectsByKey = {entry['key']: entry for entry in collectsData}

# --- Collect and Preface Lookup ---

def lookupCollect(givenDate, calendarInfo):
    label = calendarInfo['feastOrSeasonName']
    season = calendarInfo['season']
    isSunday = givenDate.weekday() == 6
    print(f"DEBUG: label = {label}")
    # 1. Try to match exact feast or day
    collectKey = matchLiturgicalDayKey(label)

    # 2. If Sunday after May 8, check for Proper X
    if not collectKey and isSunday:
        collectKey = matchProper(givenDate)

    # 3. If Ember or Rogation Day
    if not collectKey and 'Ember' in label:
        collectKey = 'emberDaysFirstOption'
    if not collectKey and 'Rogation' in label:
        collectKey = 'rogationDaysFirstOption'

    # 4. Ordinary Weekday → use previous Sunday's collect
    if not collectKey:
        lastSunday = givenDate - timedelta(days=(givenDate.weekday() + 1) % 7)
        lastSundayInfo = calendarInfoForDate(lastSunday)
        collectKey = matchLiturgicalDayKey(lastSundayInfo['feastOrSeasonName'])
        if not collectKey:
            collectKey = matchProper(lastSunday)

    print(f"DEBUG: collectKey after match = {collectKey}")

    # 5. Now get Collect and Preface
    collectEntry = collectsByKey.get(collectKey)
    if not collectEntry:
        raise ValueError(f"No collect found for {label} or date {givenDate}")

    collectText = collectEntry['collect']
    prefaceKey = collectEntry.get('preface')

    # 6. Preface fallback rules
    if not prefaceKey:
        if isSunday and season == 'Trinitytide':
            prefaceKey = 'prefaceOfTheLordsDay'
        else:
            prefaceKey = seasonalPreface(season)

    return {
        "collect": collectText,
        "prefaceKey": prefaceKey
    }

# --- Support Functions ---

def matchLiturgicalDayKey(label):
    # Exact Matches (Major Feasts, Fixed Holy Days, etc.)
    feastMapping = {
        'Christmas': 'christmasDay',
        'Epiphany': 'epiphany',
        'All Saints': 'allSaintsDay',
        'Ash Wednesday': 'ashWednesday',
        'Palm Sunday': 'palmSunday',
        'Easter': 'easterDay',
        'Ascension': 'ascensionDay',
        'Pentecost': 'dayOfPentecost',
        'Trinity Sunday': 'trinitySunday',
        'Circumcision and Holy Name': 'circumcisionAndHolyName',
        'Confession of St. Peter': 'confessionOfSaintPeter',
        'Conversion of St. Paul': 'conversionOfSaintPaul',
        'Presentation of Christ in the Temple': 'presentationOfChrist',
        'St. Matthias': 'saintMatthias',
        'St. Joseph': 'saintJoseph',
        'Annunciation': 'annunciation',
        'St. Mark': 'saintMark',
        'St. Philip and St. James': 'saintPhilipAndSaintJames',
        'Visitation': 'visitation',
        'St. Barnabas': 'saintBarnabas',
        'Nativity of John the Baptist': 'nativityOfSaintJohnTheBaptist',
        'St. Peter and St. Paul': 'saintPeterAndSaintPaul',
        'St. Mary Magdalene': 'saintMaryMagdalene',
        'St. James': 'saintJames',
        'Transfiguration': 'transfiguration',
        'The Virgin Mary': 'saintMaryTheVirgin',
        'St. Bartholomew': 'saintBartholomew',
        'Holy Cross': 'holyCrossDay',
        'St. Matthew': 'saintMatthew',
        'Holy Michael and All Angels': 'holyMichaelAndAllAngels',
        'St. Luke': 'saintLuke',
        'James of Jerusalem': 'saintJamesOfJerusalem',
        'St. Simon and St. Jude': 'saintSimonAndSaintJude',
        'St. Andrew': 'saintAndrew',
        'St. Thomas': 'saintThomas',
        'St. Stephen': 'saintStephen',
        'St. John': 'saintJohn',
        'Holy Innocents': 'holyInnocents',
        'Independence Day': 'independenceDay',
        'Thanksgiving Day': 'thanksgivingDay',
        'Memorial Day': 'memorialDayOrRemembranceDay',
        'Canada Day': 'canadaDay',
    }

    for feastName, key in feastMapping.items():
        if feastName in label:
            return key

    # Special Handling for Ember and Rogation Days
    if 'Ember' in label:
        return 'emberDaysFirstOption'
    if 'Rogation' in label:
        return 'rogationDaysFirstOption'

    # Handling for Sundays in Seasons
    if 'Sunday' in label:
        print(f"DEBUG: Checking label for Sundays in seasons: {label}")
        if 'Advent' in label:
            num = extractOrdinalNumber(label)
            if num is not None:
                return f"{ordinalWord(num)}SundayInAdvent"
        if 'Lent' in label:
            num = extractOrdinalNumber(label)
            if num is not None:
                return f"{ordinalWord(num)}SundayInLent"
        if 'Easter' in label or 'Eastertide' in label:
            num = extractOrdinalNumber(label)
            if num is not None:
                return f"{ordinalWord(num)}SundayInEaster"
        if 'Epiphany' in label and 'after' not in label:
            # This covers \"1st Sunday of Epiphany\" case if it ever appears
            num = extractOrdinalNumber(label)
            if num is not None:
                return f"{ordinalWord(num)}SundayOfEpiphany"


    # Commons (General Templates for Saints)
    commonsMapping = {
        'Common of Martyr': 'commonOfMartyr',
        'Common of Missionary': 'commonOfMissionary',
        'Common of Pastor': 'commonOfPastor',
        'Common of Teacher': 'commonOfTeacher',
        'Common of Monastic': 'commonOfMonastic',
        'Common of Ecumenist': 'commonOfEcumenist',
        'Common of Reformer': 'commonOfReformer',
        'Common of Renewer of Society': 'commonOfRenewerOfSociety',
        'Common of Any Commemoration': 'commonOfAnyCommemorationFirstOption',
    }

    for commonLabel, key in commonsMapping.items():
        if commonLabel in label:
            return key

    # If no match
    return None

def extractOrdinalNumber(label):
    import re
    print(f"DEBUG inside extractOrdinalNumber: label = {label!r}")
    match = re.search(r'(\d+)(st|nd|rd|th)', label)
    print(f"DEBUG inside extractOrdinalNumber: match = {match}")
    if match:
        return int(match.group(1))
    return None


def ordinalWord(n):
    words = {
        1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth',
        7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth',
    }
    print(f"DEBUG: Converting ordinal number {n} to word")
    return words.get(n, None)
    



def matchProper(givenDate):
    # Proper 1 = Sunday between May 8-14
    year = givenDate.year
    proper1Sunday = findProper1Sunday(year)
    weeksSinceProper1 = (givenDate - proper1Sunday).days // 7
    if weeksSinceProper1 >= 0:
        properNum = 1 + weeksSinceProper1
        if 1 <= properNum <= 29:
            return f"proper{properNum}"
    return None

def findProper1Sunday(year):
    may8 = date(year, 5, 8)
    may14 = date(year, 5, 14)
    for delta in range(7):
        d = may8 + timedelta(days=delta)
        if d.weekday() == 6:  # Sunday
            return d
    return None  # should never happen

def seasonalPreface(season):
    seasonToPreface = {
        'Advent': 'prefaceOfAdvent',
        'Christmastide': 'prefaceOfChristmas',
        'Epiphanytide': 'prefaceOfEpiphany',
        'Lent': 'prefaceOfLent',
        'Eastertide': 'prefaceOfEaster',
        'Pentecost': 'prefaceOfPentecost',
        'Trinitytide': 'prefaceOfTrinitySunday',  # fallback if needed
    }
    return seasonToPreface.get(season, None)

def calendarInfoForDate(d):
    # This would call your getLiturgicalDayDetailed from calendarEngine
    from calendarEngine import getLiturgicalDayDetailed
    return getLiturgicalDayDetailed(d)

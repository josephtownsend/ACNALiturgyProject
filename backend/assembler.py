import json
from datetime import date
from calendarEngine import getLiturgicalDayDetailed, firstSundayOfAdvent
from lookupCollect import lookupCollect

# Load the service template
with open('data/services/renewedAncientTextService.json', 'r') as f:
    serviceTemplate = json.load(f)

# Load lectionary data
try:
    with open('data/lectionary/holyDayLectionary.json', 'r') as f:
        holyDayLectionary = json.load(f)
except FileNotFoundError:
    holyDayLectionary = []

try:
    with open('data/lectionary/yearAReadings.json', 'r') as f:
        yearALectionary = json.load(f)
except FileNotFoundError:
    yearALectionary = []

try:
    with open('data/lectionary/yearBReadings.json', 'r') as f:
        yearBLectionary = json.load(f)
except FileNotFoundError:
    yearBLectionary = []

with open('data/lectionary/yearCReadings.json', 'r') as f:
    yearCLectionary = json.load(f)

# --- Helper Functions ---

def determineLectionaryYear(givenDate):
    # Determine which Advent we are in
    civilYear = givenDate.year
    adventStart = firstSundayOfAdvent(civilYear)

    if givenDate < adventStart:
        liturgicalYear = civilYear - 1
    else:
        liturgicalYear = civilYear

    # Now use liturgicalYear for modulo 3
    remainder = liturgicalYear % 3

    if remainder == 0:
        return 'A'
    elif remainder == 1:
        return 'B'
    else:
        return 'C'
    year = givenDate.year
    adventStart = firstSundayOfAdvent(year)
    if givenDate < adventStart:
        year -= 1
    remainder = year % 3
    if remainder == 0:
        return 'A'
    elif remainder == 1:
        return 'B'
    else:
        return 'C'

def lookupLessonReadings(givenDate, calendarInfo):
    label = calendarInfo['feastOrSeasonName']
    print(f"DEBUG: Label = {label}")

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
    }

    mappedKey = feastMapping.get(label)
    print(f"DEBUG: Mapped Key = {mappedKey}")

    year = determineLectionaryYear(givenDate)
    print(f"DEBUG: Lectionary Year = {year}")

    if year == 'A':
        lectionary = yearALectionary
    elif year == 'B':
        lectionary = yearBLectionary
    else:
        lectionary = yearCLectionary

    # Try Holy Day Lectionary
    if mappedKey:
        for entry in holyDayLectionary:
            print(f"DEBUG: Checking HolyDay key {entry['key']}")
            if entry['key'].lower() == mappedKey.lower():
                print(f"DEBUG: Found in HolyDayLectionary: {entry['key']}")
                return entry.get('reading') or entry.get('readingDefault')

    # Try Year Lectionary
    if mappedKey:
        for entry in lectionary:
            print(f"DEBUG: Checking YearLectionary key {entry['key']}")
            if entry['key'].lower() == mappedKey.lower():
                print(f"DEBUG: Found in YearLectionary: {entry['key']}")
                return entry.get('reading') or entry.get('readingDefault')

    # Fallback Normalize
    normalizedLabel = label.lower().replace(' ', '').replace('sunday', '').replace('day', '')
    print(f"DEBUG: Normalized Label = {normalizedLabel}")

    for entry in lectionary:
        if entry['key'].lower() == normalizedLabel:
            print(f"DEBUG: Found by Normalized Label: {entry['key']}")
            return entry.get('reading') or entry.get('readingDefault')

    print("DEBUG: No matching lessons found. Using default fallback.")
    return ["Lesson 1", "Psalm", "Epistle", "Gospel"]

    label = calendarInfo['feastOrSeasonName']

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
    }

    mappedKey = feastMapping.get(label)

    year = determineLectionaryYear(givenDate)
    if year == 'A':
        lectionary = yearALectionary
    elif year == 'B':
        lectionary = yearBLectionary
    else:
        lectionary = yearCLectionary

    # 1. Try holy day lectionary using mapped key
    if mappedKey:
        for entry in holyDayLectionary:
            if entry['key'].lower() == mappedKey.lower():
                return entry.get('reading') or entry.get('readingDefault')

    # 2. Try year lectionary using mapped key
    if mappedKey:
        for entry in lectionary:
            if entry['key'].lower() == mappedKey.lower():
                return entry.get('reading') or entry.get('readingDefault')

    # 3. Fallback: normalize label and search year lectionary
    normalizedLabel = label.lower().replace(' ', '').replace('sunday', '').replace('day', '')

    for entry in lectionary:
        if entry['key'].lower() == normalizedLabel:
            return entry.get('reading') or entry.get('readingDefault')

    return ["Lesson 1", "Psalm", "Epistle", "Gospel"]

# --- Service Assembler ---

def assembleService(givenDate):
    calendarInfo = getLiturgicalDayDetailed(givenDate)
    collectInfo = lookupCollect(givenDate, calendarInfo)
    collectText = collectInfo['collect']
    prefaceKey = collectInfo['prefaceKey']

    assembledService = []

    for element in serviceTemplate['liturgy']:
        section = {
            'id': element['id'],
            'text': ''
        }

        if element['type'] == 'static':
            text = element['text']
            if element['id'] == 'sursumCorda':
                text = text.replace("{{properPreface}}", f"[Proper Preface: {prefaceKey}]")
            section['text'] = text

        elif element['type'] == 'variableBySeason':
            season = calendarInfo['season']
            seasonOverrides = element.get('seasonOverrides', {})
            section['text'] = seasonOverrides.get(season, element.get('defaultText', ''))

        elif element['type'] == 'dynamicByCalendar':
            if element['id'] == 'collectOfTheDay':
                section['text'] = collectText
            elif element['id'] == 'lessons':
                readings = lookupLessonReadings(givenDate, calendarInfo)
                section['text'] = '\n'.join(readings)

        elif element['type'] == 'setOnce':
            defaultOption = element.get('default', '')
            section['text'] = f"Use: {defaultOption}"

        elif element['type'] == 'variableByService':
            options = element.get('options', [])
            section['text'] = f"Use: {options[0]}" if options else ''

        else:
            section['text'] = '[Unknown type]'

        assembledService.append(section)

    return assembledService

# --- Example Usage ---
if __name__ == '__main__':
    testDate = date(2024, 12, 25)  # Example: Christmas Day
    service = assembleService(testDate)

    outputLines = []
    for part in service:
        outputLines.append(f"## {part['id']}\n")
        outputLines.append(f"{part['text']}\n")

    outputMarkdown = '\n'.join(outputLines)

    with open('assembledService.md', 'w', encoding='utf-8') as f:
        f.write(outputMarkdown)

    print("Service assembled and written to assembledService.md")

import json
from datetime import date
from calendarEngine import getLiturgicalDayDetailed
from lookupCollect import lookupCollect

# Load the service template
with open('data/services/renewedAncientTextService.json', 'r') as f:
    serviceTemplate = json.load(f)

# --- Service Assembler ---

def assembleService(givenDate):
    # Step 1: Get liturgical information
    calendarInfo = getLiturgicalDayDetailed(givenDate)

    # Step 2: Get Collect and Preface
    collectInfo = lookupCollect(givenDate, calendarInfo)
    collectText = collectInfo['collect']
    prefaceKey = collectInfo['prefaceKey']

    # Step 3: Walk through service template
    assembledService = []

    for element in serviceTemplate['liturgy']:
        section = {
            'id': element['id'],
            'text': ''
        }

        if element['type'] == 'static':
            text = element['text']
            if element['id'] == 'sursumCorda':
                # Insert proper preface into Sursum Corda
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
                # TODO: Plug lectionary here
                section['text'] = 'Placeholder for scripture readings'

        elif element['type'] == 'setOnce':
            defaultOption = element.get('default', '')
            section['text'] = f"Use: {defaultOption}"

        elif element['type'] == 'variableByService':
            # Pick first option by default for now
            options = element.get('options', [])
            section['text'] = f"Use: {options[0]}" if options else ''

        else:
            section['text'] = '[Unknown type]'

        assembledService.append(section)

    return assembledService

# --- Example Usage ---
if __name__ == '__main__':
    testDate = date(2025, 12, 25)  # Example: Christmas Day
    service = assembleService(testDate)
    for part in service:
        print(f"\n== {part['id']} ==\n{part['text']}")

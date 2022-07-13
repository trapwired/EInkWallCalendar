import configparser
import requests
import datetime
import recurring_ical_events
from pytz import timezone

from icalendar import Calendar


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


if __name__ == "__main__":
    secrets = configparser.RawConfigParser()
    secrets.read('secrets.ini', encoding="utf8")
    link = secrets["Calendar"]["link2"]
    myfile = requests.get(link)

    #print(myfile.content)
    now = datetime.date.today()
    print(now)
    in7days = now + datetime.timedelta(days=7)
    gcal = Calendar.from_ical(myfile.content)
    #localtz = timezone(gcal.get('X-WR-TIMEZONE'))
    for component in gcal.walk():
        if component.name == "VTIMEZONE":
            localtz = timezone(component.get('TZID'))
    # recurring events
    events = recurring_ical_events.of(gcal).between(now, in7days)
    for event in events:
        summary = event['SUMMARY']
        startTime = event['DTSTART'].dt
        endTime = event['DTEND'].dt # TODO do the times match?
        print(summary, startTime, endTime)
    #print("HERE")
    # for component in gcal.walk():
    #     if component.name == "VEVENT":
    #         temp = component.get('dtstart').dt
    #         dateStart = temp if type(temp) == datetime.date else temp.date()
    #         if time_in_range(now, in7days, dateStart):
    #             print(component.get('summary'))
    #             print(dateStart)
    #             print(component.decoded('dtend'))
    myfile.close()

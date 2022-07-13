import configparser
import requests
import datetime
import recurring_ical_events
from pytz import timezone
import DisplayDrawer

from icalendar import Calendar


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def setup_calendar():
    secrets = configparser.RawConfigParser()
    secrets.read('secrets.ini', encoding="utf8")
    link = secrets["Calendar"]["link2"]
    myfile = requests.get(link)

    # print(myfile.content)
    now = datetime.date.today()
    print(now)
    in7days = now + datetime.timedelta(days=7)
    gcal = Calendar.from_ical(myfile.content)
    # localtz = timezone(gcal.get('X-WR-TIMEZONE'))
    for component in gcal.walk():
        if component.name == "VTIMEZONE":
            localtz = timezone(component.get('TZID'))
    # recurring events
    events = recurring_ical_events.of(gcal).between(now, in7days)
    for event in events:
        summary = event['SUMMARY']
        startTime = event['DTSTART'].dt
        endTime = event['DTEND'].dt  # TODO do the times match?
        print(summary, startTime, endTime)
    myfile.close()


if __name__ == "__main__":
    # setup_calendar()
    DisplayDrawer.start_drawing()


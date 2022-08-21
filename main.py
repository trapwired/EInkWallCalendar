import configparser
import requests
import datetime
import recurring_ical_events
from pytz import timezone
import DisplayDrawer
import schedule

from icalendar import Calendar

days_long = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def setup_calendars():
    secrets = configparser.RawConfigParser()
    secrets.read('secrets.ini', encoding="utf8")
    linkD = secrets["Calendar"]["linkD"]
    linkC = secrets["Calendar"]["linkC"]
    linkCD = secrets["Calendar"]["linkCD"]
    links = [linkD, linkC, linkCD]
    names = ['D', 'C', 'Z']

    result = []
    now = datetime.date.today()
    in5days = now + datetime.timedelta(days=5)
    for i in range(3):
        myfile = requests.get(links[i])
        gcal = Calendar.from_ical(myfile.content)
        # recurring events
        events = recurring_ical_events.of(gcal).between(now, in5days)
        for event in events:
            event['WHO'] = names[i]
        result += events
        myfile.close()

    return result


def prepare_events(even):
    # put all events in a dict from weekday to events
    whole_day_events = dict()
    normal_events = dict()
    now = datetime.date.today().weekday()
    for i in range(now, now + 5):
        whole_day_events[days[i % 7]] = []
        normal_events[days[i % 7]] = []
    # starting with today
    for event in even:
        start_time = event['DTSTART'].dt

        try:
            if type(start_time) is datetime.date:
                # whole day event
                whole_day_events[days[start_time.weekday()]].append(event)
            else:
                normal_events[days[start_time.weekday()]].append(event)
        except KeyError:
            continue

    # sort normal events
    for daysLists in normal_events:
        normal_events[daysLists] = sorted(normal_events[daysLists], key=lambda x: x['DTSTART'].dt)
    return whole_day_events, normal_events


if __name__ == "__main__":
    DisplayDrawer.setup()
    events = setup_calendars()
    wd_events, n_events = prepare_events(events)
    DisplayDrawer.start_drawing(wd_events, n_events)

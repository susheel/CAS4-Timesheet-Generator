from __future__ import print_function

import sys
import io
import datetime
import dateutil.parser

from apiclient.http import MediaIoBaseDownload

from gclient import GClient

CALENDAR_ID = "INSERT_GOOGLE_CALENDAR_ID"
DOC_ID = "INSERT_GOOGLE_DOC_ID"
TIMESHEET_RANGE = "'CAS 4'!B27:I33"
DAY2ROW = {0: 6, 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
START_DATE = "2017-04-01"

TIMESHEET_EVENTS = {}


def clear_timesheet(data=None):
    print("Clearing Timesheet.")
    c = GClient(scopes='spreadsheets')
    service = c.get_service(service_type='sheets', version='v4')

    if data is None:
        data = {'ranges': [TIMESHEET_RANGE]}

    request = service.spreadsheets().values().batchClear(spreadsheetId=DOC_ID,
                                                         body=data)
    request.execute()


def update_timesheet(rows=None):
    c = GClient(scopes='spreadsheets')
    service = c.get_service(service_type='sheets', version='v4')

    data = {
        'value_input_option': "USER_ENTERED",
        'data': [{'range': TIMESHEET_RANGE, 'values': rows}]
        }

    request = service.spreadsheets().values().batchUpdate(spreadsheetId=DOC_ID,
                                                          body=data)
    request.execute()


def download_timesheet_pdf(filename, fileId=DOC_ID):
    print("Generating Timesheet:" + filename)
    MIME_TYPE = 'application/pdf'

    c = GClient(scopes='drive.readonly')
    service = c.get_service('drive')
    request = service.files().export_media(fileId=fileId, mimeType=MIME_TYPE)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    with open(filename, 'wb') as f:
        f.write(fh.getvalue())


def build_weekly_timesheet(timesheet_events=None):
    weekly_timesheet = []
    for i in range(0, 7):
        weekly_timesheet.append(["", "", "", "", "", "", "", ""])

    for event in timesheet_events:
        day = int(event['datetime'].strftime('%w'))

        e = []
        e.append(event['date'])
        e.append(str(event['description']))
        e.extend(["", "",  ""])  # Padding
        e.append(event['start'])
        e.append(event['end'])
        e.append(event['duration'])

        weekly_timesheet[DAY2ROW[day]] = e
    return weekly_timesheet


def get_timesheet_events(start_date=None):
    print("Collecting TimeSheet Events...")
    c = GClient(scopes='calendar.readonly')
    service = c.get_service('calendar')

    try:
        timeMinDate = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except:
        print("Could not parse date string")
        sys.exit(1)
    timeMinDateISO = timeMinDate.isoformat() + 'Z'  # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId=CALENDAR_ID, timeMin=timeMinDateISO, singleEvents=True,
        showDeleted=False, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        event_end = event['end'].get('dateTime', event['end'].get('date'))

        # Calculating datetime differences
        start = dateutil.parser.parse(event_start)
        end = dateutil.parser.parse(event_end)
        diff = end - start - datetime.timedelta(hours=1)   # LUNCH = 1hr!!
        diff_hours = "{0:0>2}".format(str(diff.seconds//3600))
        diff_minutes = "{0:0>2}".format(str((diff.seconds//60) % 60))
        duration = diff_hours + ":" + diff_minutes

        week = int(start.strftime('%W'))          # Week Number
        TIMESHEET_EVENTS[week] = TIMESHEET_EVENTS.get(week, [])

        e = {}
        e['datetime'] = start
        e['date'] = start.strftime('%Y-%m-%d')
        e['description'] = str(event['summary'])
        # e.extend(["", "",  ""])                   # Padding
        e['start'] = start.strftime('%I:%M %p')
        e['end'] = end.strftime('%I:%M %p')
        e['duration'] = duration

        TIMESHEET_EVENTS[week].append(e)


def main():
    get_timesheet_events(START_DATE)
    for week, values in TIMESHEET_EVENTS.iteritems():
        rows = build_weekly_timesheet(TIMESHEET_EVENTS[week])
        update_timesheet(rows)
        download_timesheet_pdf("CAS4-Week-" + str(week) + ".pdf")
        clear_timesheet()


if __name__ == '__main__':
    main()

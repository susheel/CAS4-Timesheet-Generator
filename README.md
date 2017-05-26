## CAS4 TimeSheet Generator

Simple python script that generates a University of Manchester's CAS4 - Casual Timesheet. It uses Google Calendar to manage daily work entries and a Google Sheets doc as a template to generate a timesheet per week of the year.

### Pre-Requirements
1. Create a [new Google Calendar](https://calendar.google.com/calendar/b/0/render?tab=mc#details_2%7Cdtv-_new_calendar_id_0-0-0) and note the **Calendar ID** from it's settings.
2. Save a copy of the [CAS4 Google Sheets](https://docs.google.com/spreadsheets/d/1ZAMos4th-2YuFJPLQrvZrnPwLw68eFkzLhW1PKIMUeU/edit) document to your Google Drive. Note its new **Document ID**.
3. Prefill or modify the CAS4 template document as necessary with your details, signature, etc.
4. Update timesheet.py with the corresponding **CALENDAR ID** and **DOC ID** noted from above.
5. Generate a [project in Google Developer's Console](https://console.developers.google.com) that will be used to access various Google APIs (below) from the timesheet generation script.
5. Enable the [Google Calendar API](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview) for your project to allow the script to access calendar events.
6. Enable the [Google Drive API](https://console.developers.google.com/apis/api/drive.googleapis.com/overview) for your projectto allow the script to access the CAS4 template document.
7. Enable the [Google Sheets](https://console.developers.google.com/apis/api/sheets.googleapis.com/overview) for your project to allow the script to access the CAS4 spreadsheet template document.
8. Create a new OAuth client ID from the Google API Console [Credential page](https://console.developers.google.com/apis/credentials). Follow instructions [here](https://developers.google.com/api-client-library/python/samples/samples). Download/save the generated credentials file as client_secret.json in the root directory.

### Generating Timesheets
````
$ python generate_timesheets.py
````

### Authors
* Susheel Varma <susheel.varma@gmail.com>


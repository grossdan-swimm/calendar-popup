import datetime
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import wx
import sys

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Determine the directory of the script or executable
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_PATH = os.path.join(script_dir, 'credentials.json')
LOGFILE = os.path.join(script_dir, 'calendar_popup.log')

def log_message(msg):
    with open(LOGFILE, 'a') as f:
        f.write(f"{datetime.datetime.now().isoformat()} {msg}\n")

def get_credentials():
    print(f"[calendar_popup] credentials.json is read from: {os.path.abspath(os.path.dirname(CREDENTIALS_PATH))}")
    creds = None
    if os.path.exists(os.path.join(script_dir, 'token.pickle')):
        with open(os.path.join(script_dir, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(os.path.join(script_dir, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)
    return creds

def show_popup(event_summary, event_time, minutes_left):
    app = wx.App(False)
    frame = wx.Frame(None, title="Calendar Reminder", size=(500, 200), style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
    panel = wx.Panel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)
    label = wx.StaticText(panel, label=f"Upcoming Event:\n{event_summary}\nStarts at: {event_time}\nIn {minutes_left} minutes")
    font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    label.SetFont(font)
    label.Wrap(450)
    sizer.Add(label, 1, wx.EXPAND | wx.ALL, 20)
    btn = wx.Button(panel, label="Dismiss", size=(120, 40))
    btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    sizer.Add(btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
    panel.SetSizer(sizer)
    frame.Centre()
    frame.Raise()
    frame.Show()
    btn.Bind(wx.EVT_BUTTON, lambda event: frame.Close())
    app.MainLoop()

def main():
    log_message("calendar_popup called")
    print("[calendar_popup] Script started.")
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    print("[calendar_popup] Checking for upcoming events...")
    now = datetime.datetime.now(datetime.timezone.utc)
    time_min = now.isoformat()
    time_max = (now + datetime.timedelta(minutes=10)).isoformat()
    events_result = service.events().list(
        calendarId='primary', timeMin=time_min, timeMax=time_max,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        summary = event.get('summary', 'No Title')
        start_str = event['start'].get('dateTime', event['start'].get('date'))

        if 'T' in start_str:
            # Timed event
            if start_str.endswith('Z'):
                start_dt = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            else:
                start_dt = datetime.datetime.fromisoformat(start_str)
            if start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=datetime.timezone.utc)
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            minutes_left = int((start_dt - now_utc).total_seconds() // 60)
            event_time_str = start_dt.strftime('%Y-%m-%d %H:%M')
        else:
            # All-day event: only show if today
            event_date = datetime.datetime.fromisoformat(start_str).date()
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            if event_date == now_utc.date():
                minutes_left = 0
                event_time_str = event_date.strftime('%Y-%m-%d (all day)')
            else:
                continue  # Not today, skip

        print(f"Event: {summary}, Start: {start_str}, Now: {now_utc}, Minutes left: {minutes_left}")
        if 0 <= minutes_left < 10:
            log_message(f"Event detected: {summary} at {event_time_str} in {minutes_left} minutes.")
            print(f"[calendar_popup] Event found: {summary} at {event_time_str} in {minutes_left} minutes.")
            show_popup(summary, event_time_str, minutes_left)
            break  # Only show one popup per run
    print("[calendar_popup] Script ending.")
    sys.exit(0)

if __name__ == '__main__':
    main() 
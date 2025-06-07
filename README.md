# Calendar Popup Reminder

This program checks your Google Calendar for upcoming events in the next 10 minutes, and pops up a reminder window on macOS. It is designed to be run automatically every few minutes (5 by default) using cron.

---

## **Installation & Setup**

1. **Clone or Download the Repository**

   ```sh
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Install Python Dependencies**

   ```sh
   python3 -m pip install --user google-api-python-client google-auth-httplib2 google-auth-oauthlib wxPython python-crontab pyinstaller
   ```

3. **Set Up Google API Credentials**

   - Go to the [Google Cloud Console](https://console.developers.google.com/).
   - Enable the Google Calendar API and download your `credentials.json`.
   - Place `credentials.json` in the same folder as the program.

4. **Create the Executable**

   ```sh
   pyinstaller --onefile calendar_popup.py
   ```

   - The executable will be created in the `dist/` folder (e.g., `dist/calendar_popup`).

5. **Prepare the Executable Folder**

   - Create a folder for your executable, e.g., `/Users/dani/dist/`
   - Copy the following files into this folder:
     - The executable (`calendar_popup`)
     - `credentials.json`
     - `token.pickle` (this will be created after your first run and authentication)

   Example:
   ```sh
   mkdir -p /Users/dani/dist
   cp dist/calendar_popup /Users/dani/dist/
   cp credentials.json /Users/dani/dist/
   # token.pickle will be created after first run
   ```

6. **First Run (Authenticate with Google)**

   - Run the executable once to authenticate and generate `token.pickle`:
     ```sh
     cd /Users/dani/dist
     ./calendar_popup
     ```
   - A browser window will open for you to log in and authorize access.

---

## **Scheduling with Cron**

- The program is designed to be run by cron every 5 minutes (recommended), so you get a popup 10 minutes before and again 5 minutes before an event.

### **Set Up Cron with manage_cron.py**

- **Double-click** `manage_cron` (if your system is set up to run Python scripts this way), or
- **Open a terminal** and run:

  ```sh
  ./manage_cron
  ```

  This will set the cron job to run every 5 minutes by default.

- **To change the interval**, specify the number of minutes:

  ```sh
  ./manage_cron.py 10
  ```

- **To remove the cron job (needs to be done in terminal):**

  ```sh
  ./manage_cron.py 0
  ```

---

## **How the Reminder Works**

- The popup will appear 10 minutes before an event, and again every time cron runs (e.g., 5 minutes before, if using a 5-minute interval).
- For best results, keep the interval at 5 minutes.

---

## **Log File**

- The program writes logs to `calendar_popup.log` in the same folder as the executable.

- Automatic Log Rotation:

At the start of each new day, the log file is cleared and a backup of the previous day's log is saved as calendar_popup.log.bak. Only one backup copy is kept at a time.

When the log is rotated, a message is written to the new log file indicating the log was cleared and a backup was made.
---

## **Notes**

- Make sure `credentials.json` and `token.pickle` are in the same folder as the executable.
- The first run will require Google authentication in your browser.
- The program will only show a popup if an event is within the next 10 minutes, and then every time cron runs the pop up reminder.

---

**Enjoy your automatic calendar reminders!**

2024-06-07T00:00:01 Log cleared for new day, backup saved as calendar_popup.log.bak

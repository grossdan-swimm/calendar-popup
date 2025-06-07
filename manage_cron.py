import sys
from crontab import CronTab

CRON_COMMAND = '/Users/dani/dist/calendar_popup'

if len(sys.argv) == 1:
    minutes = 5
elif len(sys.argv) == 2:
    try:
        minutes = int(sys.argv[1])
    except ValueError:
        print("Argument must be an integer.")
        sys.exit(1)
else:
    print("Usage: python manage_cron.py <minutes>")
    sys.exit(1)

cron = CronTab(user=True)

if minutes > 0:
    # Remove any existing jobs for this command
    cron.remove_all(command=CRON_COMMAND)
    # Add new job
    job = cron.new(command=CRON_COMMAND)
    job.setall(f"*/{minutes} * * * *")
    cron.write()
    print(f"Cron job set to run every {minutes} minute(s).")
elif minutes == 0:
    cron.remove_all(command=CRON_COMMAND)
    cron.write()
    print("Cron job removed.")
else:
    print("Minutes must be zero or a positive integer.")
    sys.exit(1) 
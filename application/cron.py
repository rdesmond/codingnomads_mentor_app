from crontab import CronTab


# Command for importing users from the Moodle DB
response = request.get('URL')

# Accessing cron
cron = CronTab(user='roger')

job = cron.new(command=users_import.py)

job.hour.ever(4)

cron.write()

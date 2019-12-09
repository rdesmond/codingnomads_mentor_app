from crontab import CronTab

user = 'roger'
# Accessing cron
cron = CronTab(user=user)

user_import = cron.new(command='new_users.py')

user_import.hour.every(12)

cron.write()

user_update = cron.new(command='update.py')

user_update.hour.ever(24)

cron.write()


from apscheduler.schedulers.blocking import BlockingScheduler
from main import temp_and_dec, temp_only
import random
import time

sched = BlockingScheduler()

# start_time = time.time()

# Run morning tasks - Daily Declaration + Record Temperature (Runs between 07:28 and 09:28)
sched.add_job(temp_and_dec, 'cron', hour=7, minute=28, jitter=3600, misfire_grace_time=None, timezone="Singapore")

# Run afternoon task - Record Temperature (Runs between 17:38 and 19:38)
sched.add_job(temp_only, 'cron', hour=17, minute=38, jitter=3600, misfire_grace_time=None, timezone="Singapore")

sched.start()
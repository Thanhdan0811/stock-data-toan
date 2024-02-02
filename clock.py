from apscheduler.schedulers.blocking import BlockingScheduler
from main import call_stock
import pytz

sched = BlockingScheduler()

# @sched.scheduled_job('interval', seconds=15)
# def timed_job():
#     print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week="mon,tue,wed,thu,fri,sat,sun" ,hour=22, minute=15, timezone=pytz.timezone("Asia/Ho_Chi_Minh"))
def scheduled_job():
    call_stock()
    print('This job is run every weekday at 5pm.')

sched.start()
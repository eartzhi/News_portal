import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'every_week_notification':{
        'task': 'news.tasks.weekly_notificator',
        'schedule': crontab(minute=0, hour=8, day_of_week='monday'),
        'args': (),
    }
}
app.autodiscover_tasks()
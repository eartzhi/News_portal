import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Moscow'
app.conf.beat_schedule = {
    'every_week_notification':{
        'task': 'news.tasks.weekly_notificator',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    }
}
app.autodiscover_tasks()
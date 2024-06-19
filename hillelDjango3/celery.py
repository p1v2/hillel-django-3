import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CourseDjango.settings')

app = Celery('CourseDjango')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.CELERY_BEAT_SCHEDULE = {
    'daily_orders_count': {
        'task': 'CourseDjango.tasks.daily_order_count',
        'schedule': crontab(hour=10),
    }
}
import datetime
import logging
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category
from news.signals import email_sender

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    period_end = timezone.now()
    period_start = period_end - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_time__gte=period_start)
    subscribers_email = list(set(posts.
                                 values_list('category__subscriber__email',
                                             flat=True)))

    for email in subscribers_email:
        if email is not None:
            user_categories = User.objects.filter(email=email).\
                values_list('category', flat=True)
            user_posts = set(posts.filter(category__in=user_categories))

            html_content = render_to_string(
                'weekly_notification.html',
                {
                'posts': user_posts,
                'SITE_URL': settings.SITE_URL

                }
            )
            time.sleep(3)  # достал меня яндекс спам фильтр
            email_sender(subject='Еженедельная рассылка',
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         recipient_list=[email],
                         html_content=html_content)


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='sun', hour='17', minute='00'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

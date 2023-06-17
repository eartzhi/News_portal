from celery import shared_task
from .signals import email_sender
import time
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import Post, Category
import datetime
from django.contrib.auth.models import User


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)


@shared_task
def post_create_notify(post, **kwargs):
    html_content = render_to_string(
        'email_notification.html',
        {
            'text': post.text[:50],
            'link': f'{settings.SITE_URL}/posts/{post.pk}'

        }
    )
    subscribers_emails = []
    if kwargs['action'] == 'post_add':
        categories = post.category.all()

        for category in categories:
            subscribers = category.subscriber.all()
            for subscriber in subscribers:
                subscribers_emails += [subscriber.email]

    for email in set(subscribers_emails):
        if email is not None:
            time.sleep(3) # достал меня яндекс спам фильтр
            email_sender(subject=post.header,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         recipient_list=[email],
                         html_content=html_content)


def weekly_notificator():
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
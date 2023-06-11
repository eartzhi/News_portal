from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, PostCategory
from django.conf import settings


def email_sender(subject, from_email, recipient_list, html_content):
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',  # это то же, что и message
        from_email=from_email,
        to=recipient_list,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем


@receiver(m2m_changed, sender=PostCategory)
def post_create_notify(sender, instance, **kwargs):
    html_content = render_to_string(
        'email_notification.html',
        {
            'text': instance.text[:50],
            'link': f'{settings.SITE_URL}/posts/{instance.pk}'

        }
    )
    subscribers_emails = []
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()

        for category in categories:
            subscribers = category.subscriber.all()
            for subscriber in subscribers:
                subscribers_emails += subscriber.email
    email_sender(subject=instance.text[:50],
                 from_email=settings.EMAIL_DEFAULT_FROM_EMAIL,
                 recipient_list=subscribers_emails, html_content=html_content)

    # for email in subscribers_emails:
    #     email_sender(subject=instance.text[:50],
    #                  from_email= settings.EMAIL_DEFAULT_FROM_EMAIL,
    #                  recipient_list=email, html_content= html_content)

    # send_mail(
    #     subject=f'bla bla ,la',
    #     # имя клиента и дата записи будут в теме для удобства
    #     message='bla bla ,la',  # сообщение с кратким описанием проблемы
    #     from_email='news.portalzhigunov@yandex.ru',
    #     # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #     recipient_list=['zhigunovam@gmail.com', ]
    #     # здесь список получателей. Например, секретарь, сам врач и т. д.
    # )

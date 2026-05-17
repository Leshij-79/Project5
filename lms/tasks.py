from smtplib import SMTPException

from celery import shared_task
from django.core.mail import send_mail
from icecream import ic
from rest_framework.response import Response

from config import settings
from lms.models import Subscriptions


@shared_task
def send_email_update(data):
    mailing = Subscriptions.objects.filter(course=data['course']).all()

    result = []

    for mail_send in mailing:
        try:
            server_response = send_mail(
                subject=f'Обновление курса {mail_send.course.title}',
                message=f'Пользователь {mail_send.user.first_name} {mail_send.user.last_name} сообщаем, '
                        f'что курс {mail_send.course.title} обновился',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[mail_send.user.email,],
            )

            if server_response == 1:
                result.append(f"Письмо принято SMTP-сервером на адрес {mail_send.user.email}")
            else:
                result.append("Неизвестная ошибка отправки")

        except SMTPException as e:
            result.append(f"Ошибка SMTP: {str(e)}")

        except Exception as e:
            result.append(f"Внутренняя ошибка сервера: {str(e)}")

    return result


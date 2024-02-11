from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from mailing_service.models import MailingList, Log
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)


def send_messages(mailing_list):
    clients = mailing_list.clients.all()
    for client in clients:
        send_mail(
            subject='Отправка письма',
            message=f'текст письма',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email],
            fail_silently=False
        )
        print('send mail')

        Log.objects.create(
            mailing_list_id=mailing_list.id,
            status='success',
        )


@register_job(scheduler, "cron", day_of_week='*', hour='*', minute='53')
def my_scheduled_task():
    print('add task')
    current_time = timezone.now()
    mailing_lists = MailingList.objects.all()

    for mailing_list in mailing_lists:
        if mailing_list.start_time <= current_time <= mailing_list.end_time:
            # Проверяем, не наступило ли время отправки в соответствии с частотой
            if mailing_list.status != 'completed' or mailing_list.status != 'disable':
                time_difference = current_time - mailing_list.start_time

                if mailing_list.frequency == 'daily' and time_difference.days % 1 == 0:
                    send_messages(mailing_list)

                elif mailing_list.frequency == 'weekly' and time_difference.days % 7 == 0:
                    send_messages(mailing_list)

                elif mailing_list.frequency == 'monthly' and current_time.day == mailing_list.start_time.day:
                    send_messages(mailing_list)

        mailing_list.status = 'completed' if current_time > mailing_list.end_time else 'started'
        mailing_list.save()


scheduler.start()

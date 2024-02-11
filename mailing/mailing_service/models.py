from django.db import models
from django.conf import settings


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.full_name}: {self.email}'


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class MailingList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    frequency_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    frequency = models.CharField(max_length=10, choices=frequency_choices)

    status_choices = [
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('disable', 'Disable'),
    ]
    status = models.CharField(
        max_length=10, choices=status_choices, default='created')

    clients = models.ManyToManyField(Client)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)


class Log(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    server_response = models.TextField(null=True, blank=True)

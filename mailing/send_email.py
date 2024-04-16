import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing_service.settings')
import django
django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from mailing.models import Mailing, Client, Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils import timezone
from datetime import datetime


# Настройки для подключения к SMTP-серверу Mail.ru
smtp_server = 'smtp.mail.ru'
smtp_port = 587  # Порт SMTP-сервера Mail.ru
email_address = 'skyprokutalov.k.v@mail.ru'
email_password = 'ud8KsqPUJmPxwHEXJbWd'


def send_email(recipient_email, subject, body):
    try:
        # Установка соединения с SMTP-сервером Mail.ru
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)  # Аутентификация на сервере

        # Формирование сообщения
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Отправка письма
        server.sendmail(email_address, recipient_email, msg.as_string())

        print(f"Письмо успешно отправлено для {recipient_email}")
        server.quit()
        return True
    except Exception as e:
        print(f"Ошибка отправки письма для {recipient_email}:", e)
        return False


def send_emails_to_recipients():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Очередь рассылки:")
    # Получаем все рассылки, которые должны быть отправлены на данный момент
    mailings_to_send = Mailing.objects.filter(status='sent', send_datetime__lte=timezone.now())

    for mailing in mailings_to_send:
        print(f"Рассылка {mailing} выполнена в {now}")
        # Получаем всех клиентов, которым нужно отправить это сообщение
        clients = mailing.clients.all()
        message = mailing.message

        for client in clients:
            send_email(client.email, message.subject, message.body)

        # После отправки устанавливаем статус рассылки в "Отправлено"
        mailing.status = 'cancelled'
        mailing.save()


# Создаем планировщик задач
scheduler = BackgroundScheduler()

# Устанавливаем расписание для отправки писем
scheduler.add_job(send_emails_to_recipients, 'interval', minutes=1)  # Проверяем каждую минуту

# Запускаем планировщик
scheduler.start()

# Необходимо удерживать основной поток выполнения активным
try:
    while True:
        pass
except KeyboardInterrupt:
    scheduler.shutdown()

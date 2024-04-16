from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients', default=10)

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', default=10)



    def __str__(self):
        return self.subject


class Mailing(models.Model):
    SEND_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]
    send_datetime = models.DateTimeField()
    frequency = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=SEND_CHOICES, default='draft')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')
    clients = models.ManyToManyField(Client, related_name='mailings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mailings', default=10)

    def __str__(self):
        return f"Mailing {self.id}"


class SendingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]
    sending_datetime = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response = models.TextField(blank=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='sending_attempts')

    def __str__(self):
        return f"Attempt for {self.mailing} at {self.sending_datetime}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    views = models.IntegerField(default=0)
    publish_date = models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('mailing:blog_post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


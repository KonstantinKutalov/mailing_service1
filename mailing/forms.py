from django import forms
from .models import Client, Mailing, Message, BlogPost


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['send_datetime', 'frequency', 'status', 'message', 'clients']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'publish_date']

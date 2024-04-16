from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Client, Mailing, Message, SendingAttempt, BlogPost
from .forms import ClientForm, MailingForm, MessageForm, BlogPostForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.views.generic import CreateView


# Для не авторизованых
def registration_required(request):
    return render(request, 'registration_required.html')


# Декоратор для проверки владельца объекта
def owner_required(model):
    def decorator(view_func):
        @method_decorator(login_required)
        def wrapper(self, request, pk, *args, **kwargs):
            obj = get_object_or_404(model, pk=pk)
            if obj.owner != request.user:
                return HttpResponseForbidden("У вас нет доступа к этому объекту.")
            return view_func(self, request, pk, *args, **kwargs)

        return wrapper

    return decorator


# home и все что связано с ним

class HomeView(TemplateView):
    template_name = 'home.html'


# Клиент

class ClientListView(View):
    @method_decorator(login_required)
    def get(self, request):
        clients = Client.objects.filter(owner=request.user)
        return render(request, 'client_list.html', {'clients': clients})


class ClientDetailView(View):
    @method_decorator(owner_required(Client))
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        return render(request, 'client_detail.html', {'client': client})


class ClientCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ClientForm()
        return render(request, 'client_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect('mailing:client_list')
        return render(request, 'client_form.html', {'form': form})


class ClientUpdateView(View):
    @method_decorator(owner_required(Client))
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(instance=client)
        return render(request, 'client_form.html', {'form': form})

    @method_decorator(owner_required(Client))
    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, 'client_form.html', {'form': form})


class ClientDeleteView(View):
    @method_decorator(owner_required(Client))
    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        return render(request, 'client_confirm_delete.html', {'client': client})

    @method_decorator(owner_required(Client))
    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return redirect('mailing:client_list')


# Рассылки

class MailingListView(View):
    @method_decorator(login_required)
    def get(self, request):
        mailings = Mailing.objects.filter(owner=request.user)
        return render(request, 'mailing_list.html', {'mailings': mailings})


class MailingDetailView(View):
    @method_decorator(owner_required(Mailing))
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        return render(request, 'mailing_detail.html', {'mailing': mailing})


class MailingCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = MailingForm()
        return render(request, 'mailing_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            return redirect('mailing:mailing_list')
        return render(request, 'mailing_form.html', {'form': form})


class MailingUpdateView(View):
    @method_decorator(owner_required(Mailing))
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(instance=mailing)
        return render(request, 'mailing_form.html', {'form': form})

    @method_decorator(owner_required(Mailing))
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing:mailing_list')
        return render(request, 'mailing_form.html', {'form': form})


class MailingDeleteView(View):
    @method_decorator(owner_required(Mailing))
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        return render(request, 'mailing_confirm_delete.html', {'mailing': mailing})

    @method_decorator(owner_required(Mailing))
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.delete()
        return redirect('mailing:mailing_list')


# Сообщения

class MessageListView(View):
    @method_decorator(login_required)
    def get(self, request):
        messages = Message.objects.filter(owner=request.user)
        return render(request, 'message_list.html', {'messages': messages})


class MessageDetailView(View):
    @method_decorator(owner_required(Message))
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        return render(request, 'message_detail.html', {'message': message})


class MessageCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = MessageForm()
        return render(request, 'message_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.owner = request.user
            message.save()
            return redirect('mailing:message_list')
        return render(request, 'message_form.html', {'form': form})


class MessageUpdateView(View):
    @method_decorator(owner_required(Message))
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(instance=message)
        return render(request, 'message_form.html',
                      {'form': form, 'message': message})  # Передаем экземпляр сообщения в контекст шаблона

    @method_decorator(owner_required(Message))
    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('mailing:message_list')
        return render(request, 'message_form.html', {'form': form, 'message': message})


class MessageDeleteView(View):
    @method_decorator(owner_required(Message))
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        return render(request, 'message_confirm_delete.html', {'message': message})

    @method_decorator(owner_required(Message))
    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return redirect('mailing:message_list')


def add_mailing(request):
    clients = Client.objects.filter(owner=request.user)
    print(clients)  # Отладочный вывод данных о клиентах в консоль
    return render(request, 'mailing_form.html', {'clients': clients})


# Менеджеры
class ManagerView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Менеджеры').exists()))
    def get(self, request):
        return render(request, 'managers/manager_view.html')


class BlockUserView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Менеджеры').exists()))
    def get(self, request):
        users = User.objects.all()  # Получаем список всех пользователей
        return render(request, 'managers/block_user.html', {'users': users})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Менеджеры').exists()))
    def post(self, request):
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.is_active = False  # Блокируем пользователя
        user.save()
        return redirect('manager_view')


class DisableMailingView(View):
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Менеджеры').exists()))
    def get(self, request):
        mailings = Mailing.objects.all()  # Получаем список всех рассылок
        return render(request, 'managers/disable_mailing.html', {'mailings': mailings})

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Менеджеры').exists()))
    def post(self, request):
        mailing_id = request.POST.get('mailing_id')
        mailing = get_object_or_404(Mailing, id=mailing_id)
        mailing.status = 'disabled'  # Отключаем рассылку
        mailing.save()
        return redirect('manager_view')


# Блог
class BlogPostListView(View):
    def get(self, request):
        posts = BlogPost.objects.all()
        return render(request, 'blog/blog_post_list.html', {'posts': posts})


class BlogPostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        return render(request, 'blog/blog_post_detail.html', {'post': post})


class BlogPostCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = BlogPostForm()
        return render(request, 'blog/blog_post_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blog_post_list')
        return render(request, 'blog/blog_post_form.html', {'form': form})


class BlogPostUpdateView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        form = BlogPostForm(instance=post)
        return render(request, 'blog/blog_post_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_post_list')
        return render(request, 'blog/blog_post_form.html', {'form': form})


class BlogPostDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        return render(request, 'blog/blog_post_confirm_delete.html', {'post': post})

    @method_decorator(login_required)
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        post.delete()
        return redirect('blog_post_list')


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content']
    template_name = 'blog/blog_post_create.html'

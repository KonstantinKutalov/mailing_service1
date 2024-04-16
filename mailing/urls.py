from django.urls import path, include
from django.contrib import admin
from . import views
from .views import (
    ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    HomeView, add_mailing,
)

app_name = 'mailing'

urlpatterns = [
    # URL-home и прочее
    path('', HomeView.as_view(), name='home'),

    # URL-адреса для Клиентов
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    # URL-адреса для Рассылок
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('add_mailing/', add_mailing, name='add_mailing'),

    # URL-адреса для Сообщений
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # Регистрация, Вход
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/registration_required/', views.registration_required, name='registration_required'),

    # Менеджеры
    path('manager/', views.ManagerView.as_view(), name='manager_view'),
    path('block_user/', views.BlockUserView.as_view(), name='block_user'),
    path('disable_mailing/', views.DisableMailingView.as_view(), name='disable_mailing'),

    # Блог
    # Список статей
    path('posts/', views.BlogPostListView.as_view(), name='blog_post_list'),

    # Детальный просмотр статьи
    path('posts/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),

    # Создание новой статьи
    path('posts/create/', views.BlogPostCreateView.as_view(), name='blog_post_create'),

    # Редактирование статьи
    path('posts/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='blog_post_update'),

    # Удаление статьи
    path('posts/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_post_delete'),

]

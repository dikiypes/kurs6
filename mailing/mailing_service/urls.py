# urls.py

from django.urls import path
from .views import CreateMailingView
from .views import ManageClientsView, EditClientView, DeleteClientView
from .views import CreateMailingView, ManageClientsView, EditClientView, DeleteClientView, CreateMessageView, EditMessageView, DeleteMessageView, ManageMessagesView, EditMailingView, DeleteMailingView, ManageMailingsView, DisableMailingView
import mailing_service.scheduler
app_name = 'mailing_service'


urlpatterns = [
    path('manage_clients/', ManageClientsView.as_view(), name='manage_clients'),
    path('edit_client/<int:pk>/', EditClientView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>/',
         DeleteClientView.as_view(), name='delete_client'),
    path('create_mailing/', CreateMailingView.as_view(), name='create_mailing'),
    path('create_message/', CreateMessageView.as_view(), name='create_message'),
    path('edit_message/<int:pk>/', EditMessageView.as_view(), name='edit_message'),
    path('delete_message/<int:pk>/',
         DeleteMessageView.as_view(), name='delete_message'),
    path('manage_messages/', ManageMessagesView.as_view(), name='manage_messages'),
    path('edit_mailing/<int:pk>/', EditMailingView.as_view(), name='edit_mailing'),
    path('delete_mailing/<int:pk>/',
         DeleteMailingView.as_view(), name='delete_mailing'),
    path('disable_mailing/<int:pk>/',
         DisableMailingView.as_view(), name='delete_mailing'),
    path('manage_mailings/', ManageMailingsView.as_view(), name='manage_mailings'),
]

from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmView, EmailConfirmationFailedView, UserForgotPasswordView, UserListView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(),
         name='email_confirmation_sent'),  # Письмо подтверждения отправлено
    path('confirm-email/<str:token>/', UserConfirmEmailView.as_view(),
         name='email_verified'),  # работа с токеном
    path('email-confirmed/', EmailConfirmView.as_view(),
         name='email_verified'),  # Электронная почта подтверждена
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(),
         name='email_confirmation_failed'),  # Ошибка подтверждения по электронной почте

    path('password_reset/', UserForgotPasswordView.as_view(),
         name='password_reset'),  # забыл пароль
    path('user_list/', UserListView.as_view(), name='user_list'),

]

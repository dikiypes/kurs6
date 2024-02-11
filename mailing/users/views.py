from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, reverse_lazy, PasswordResetConfirmView
from django.contrib.auth import login
from .forms import UserRegisterForm, UserForgotPasswordForm, UserSetNewPasswordForm
from django.views.generic import UpdateView, CreateView, TemplateView
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.views import View
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
import secrets
import string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.requests import RequestSite
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались. Проверьте почту для активации!'

    def form_valid(self, form):
        # Сохраняем форму, чтобы получить доступ к данным
        response = super().form_valid(form)

        # Получаем выбранную роль из формы
        role = form.cleaned_data.get('role')

        group_name = 'Пользователи'
        print('user role:', role)
        # Определяем группу в зависимости от роли (замените на свои значения)
        if role == 'manager':
            group_name = 'Менеджеры'
        elif role == 'user':
            group_name = 'Пользователи'

        # Добавляем пользователя в соответствующую группу
        group = Group.objects.get(name=group_name)
        self.object.groups.add(group)

        # Остальной код для отправки подтверждающего письма
        user = form.instance
        user.is_active = False
        user.token = default_token_generator.make_token(user)
        activation_url = reverse_lazy(
            'users:email_verified', kwargs={'token': user.token}
        )
        user.save()

        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: http://localhost:8000/{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )

        return response


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        next_url = self.request.GET.get('next')

        # Проверяем, является ли URL безопасным
        if next_url and next_url.startswith('/'):
            return HttpResponseRedirect(next_url)
        else:
            # Перенаправляем на URL по умолчанию, если URL не является безопасным
            return HttpResponseRedirect(reverse('mailing_service:manage_mailings'))


class UserLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    success_url = reverse_lazy('mailing_service:manage_mailings')


class UserConfirmEmailView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return redirect('users:email_confirmation_failed')

        user.is_active = True
        user.token = None
        user.save()
        return redirect('users:login')


class EmailConfirmationSentView(TemplateView):
    """Письмо подтверждения отправлено"""
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmView(TemplateView):
    """Электронная почта подтверждена"""
    template_name = 'registration/email_verified.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    """Ошибка подтверждения по электронной почте"""
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


def generate_random_password(length=12):
    """Генерация случайного пароля"""
    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(secrets.choice(characters) for _ in range(length))
    return new_password


class UserForgotPasswordView(PasswordResetView):
    """Востановление пароля"""
    model = User
    form_class = UserForgotPasswordForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('users:login')
    email_template_name = 'registration/password_reset_mail.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)

        new_password = generate_random_password()
        user.set_password(new_password)
        user.save()

        context = {
            'user': user,
            'new_password': new_password
        }

        email_content = render_to_string(self.email_template_name, context)

        send_mail(
            subject='Восстановление пароля',
            message=email_content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super(FormView, self).form_valid(form)


class UserListView(ListView):
    model = User
    template_name = 'registration/user_list.html'
    context_object_name = 'users'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_role = request.user.role
        if user_role == 'manager':
            users_list = User.objects.all()
            return render(request, self.template_name, {'users_list': users_list})
        else:
            return render(request, 'registration/no_access.html')

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        user = User.objects.get(pk=request.POST['user_id'])
        is_active = user.is_active
        print(is_active)
        if is_active:
            user.is_active = False
        else:
            user.is_active = True

        user.save()
        return redirect('users:user_list')

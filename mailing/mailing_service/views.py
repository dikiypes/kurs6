from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import MailingForm, ClientForm, MessageForm
from .models import Client, Message, MailingList
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class ManageClientsView(View):
    template_name = 'manage_clients.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        clients = Client.objects.filter(user=request.user)
        form = ClientForm()
        return render(request, self.template_name, {'clients': clients, 'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
        if form.is_valid():
            client_item = form.save(commit=False)
            client_item.user = request.user
            client_item.save()
            return redirect('mailing_service:manage_clients')

        clients = Client.objects.filter(user=request.user)
        return render(request, self.template_name, {'clients': clients, 'form': form})


class EditClientView(View):
    template_name = 'edit_client.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(instance=client)
        return render(request, self.template_name, {'form': form, 'client': client})

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        client = get_object_or_404(Client, pk=pk)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('mailing_service:manage_clients')

        return render(request, self.template_name, {'form': form, 'client': client})


class DeleteClientView(View):
    template_name = 'delete_client.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=kwargs['pk'])
        return render(request, self.template_name, {'client': client})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=kwargs['pk'])
        client.delete()
        return redirect('mailing_service:manage_clients')


class CreateMessageView(View):
    template_name = 'create_message.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = MessageForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailing_service:manage_messages')
        return render(request, self.template_name, {'form': form})


class EditMessageView(View):
    template_name = 'edit_message.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        form = MessageForm(instance=message)
        return render(request, self.template_name, {'form': form, 'message': message})

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        user_role = request.user.role
        if user_role != 'manager':
            message = get_object_or_404(Message, pk=pk)
            form = MessageForm(request.POST, instance=message)
            if form.is_valid():
                form.save()
                return redirect('mailing_service:manage_messages')
            return render(request, self.template_name, {'form': form, 'message': message})
        else:
            return render(request, 'registration/no_access.html')


class DeleteMessageView(View):
    template_name = 'delete_message.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        return render(request, self.template_name, {'message': message})

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return redirect('mailing_service:manage_messages')


class ManageMessagesView(View):
    template_name = 'manage_messages.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        messages = Message.objects.all()
        return render(request, self.template_name, {'messages': messages})


class CreateMailingView(View):
    template_name = 'create_mailing.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = MailingForm(request.user)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = MailingForm(request.user, request.POST)
        if form.is_valid():
            mailing_item = form.save(commit=False)
            mailing_item.user = request.user
            mailing_item.save()
            return redirect('mailing_service:manage_mailings')
        return render(request, self.template_name, {'form': form})


class EditMailingView(View):
    template_name = 'edit_mailing.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(MailingList, pk=pk)
        form = MailingForm(instance=mailing)
        return render(request, self.template_name, {'form': form, 'mailing': mailing})

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        user_role = request.user.role
        if user_role != 'manager':
            mailing = get_object_or_404(MailingList, pk=pk)
            form = MailingForm(request.POST, instance=mailing)
            if form.is_valid():
                form.save()
                return redirect('mailing_service:manage_mailings')

            return render(request, self.template_name, {'form': form, 'mailing': mailing})
        else:
            return render(request, 'registration/no_access.html')


class DeleteMailingView(View):
    template_name = 'delete_mailing.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        mailing = get_object_or_404(MailingList, pk=pk)
        return render(request, self.template_name, {'mailing': mailing})

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        user_role = request.user.role
        if user_role != 'manager':
            mailing = get_object_or_404(MailingList, pk=pk)
            mailing.delete()
            return redirect('mailing_service:manage_mailings')
        else:
            return render(request, 'registration/no_access.html')


class DisableMailingView(View):
    template_name = 'delete_mailing.html'

    @method_decorator(login_required)
    def get(self, request, pk, *args, **kwargs):
        user_role = request.user.role
        if user_role == 'manager':
            mailing = get_object_or_404(MailingList, pk=pk)
            return render(request, self.template_name, {'mailing': mailing})
        else:
            return render(request, 'registration/no_access.html')

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        user_role = request.user.role
        if user_role == 'manager':
            mailing = get_object_or_404(MailingList, pk=pk)
            # Изменение статуса на "disable"
            mailing.status = 'disable'
            mailing.save()
            return redirect('mailing_service:manage_mailings')
        else:
            return render(request, 'registration/no_access.html')


class ManageMailingsView(View):
    template_name = 'manage_mailings.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user_role = request.user.role
        if user_role == 'manager':
            mailings = MailingList.objects.all()
        else:
            mailings = MailingList.objects.filter(user=request.user)
        return render(request, self.template_name, {'mailings': mailings})

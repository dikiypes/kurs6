from django import forms
from .models import MailingList, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ['start_time', 'end_time',
                  'frequency', 'status', 'message', 'clients']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(user=user)

    start_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    end_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    frequency = forms.ChoiceField(
        choices=MailingList.frequency_choices,
        widget=forms.Select(attrs={'placeholder': 'Select frequency'}),
    )

    status = forms.ChoiceField(
        choices=MailingList.status_choices,
        widget=forms.Select(attrs={'placeholder': 'Select status'}),
    )

    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
    )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class ManageClientsForm(forms.Form):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    new_client = ClientForm()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }

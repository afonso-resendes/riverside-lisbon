from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import reservas_Coworking_provisoria
        
class CreateUserForm(UserCreationForm):
    error_css_class = 'error'
    first_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=16)
    email = forms.CharField(max_length=75, required=True)

    def clean_username(self):
        data = self.cleaned_data['username']

        if not data.islower():
            raise forms.ValidationError("Username should be in lowercase")
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'first_name', 'last_name']

        widgets = {
            'email': forms.TextInput(attrs={'id': 'email'}),
            'username': forms.TextInput(attrs={'id': 'username'}),
            'password1': forms.PasswordInput(attrs={'id': 'pass'}),
            'password2': forms.PasswordInput(attrs={'id': 'confirm'}),
        }


class ReservaModelForm(forms.ModelForm):
    class Meta:
        model = reservas_Coworking_provisoria
        fields = (
            "startDate",
            "chair1",
            "chair2",
            "chair3",
            "chair4",
            "chair5",
            "chair6",
            "chair7",
            "chair8",
            "chair9",
            "chair10",
            "chair11",
            "chair12",
        )

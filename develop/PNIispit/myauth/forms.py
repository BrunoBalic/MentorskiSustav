from django import forms
from django.forms import ModelForm
from django.forms import ValidationError
from django.contrib.auth import authenticate

from users.models import Users


class MyAuthenticationForm(ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Users
        fields = (
            'email',
            'password',
        )

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                print("login nije uspio")
                raise forms.ValidationError("Email ili lozinka nije tocna!")

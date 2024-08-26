from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User  # Make sure to import your custom User model

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True, help_text='Required. Add a valid email address.')
    first_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=100, required=True, help_text='Required. Enter your last name.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

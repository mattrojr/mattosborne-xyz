from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email=forms.CharField(
        help_text="Required for password recovery",
        required=True
    )
    first_name=forms.CharField(
        help_text="Optional",
        required=False
    )
    last_name=forms.CharField(
        help_text="Optional",
        required=False
    )
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

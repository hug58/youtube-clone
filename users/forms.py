from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2'] 
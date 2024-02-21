from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta: # Gives us a nested namespace
        model = User # It will save it into this user model
        fields = ['username', 'email', 'password1', 'password2'] # Set fields in order

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    '''form of identification'''
    username = forms.CharField(max_length=63, label="nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput,
                               label="mot de passe")


class SignupForm(UserCreationForm):
    '''user profile creation form'''
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {"username": "nom d'utilisateur",
                  "first_name": "prénom",
                  "last_name": "nom"}

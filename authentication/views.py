from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect

from . import forms

def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('reviews-home')
            else:
                message = 'Identifiant ou mot de passe invalide'
    return render(
        request, "login.html", context={"form": form, "message": message}
    )

User = get_user_model()

def signup(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('reviews-home')
    return render(request, "signup.html", context={'form': form})

def logout_user(request):
    logout(request)
    return redirect('authentication_login_page')

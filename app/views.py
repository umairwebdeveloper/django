import os
import json
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required


def load_json_file(file_path):
    absolute_path = os.path.join(settings.BASE_DIR, file_path)
    with open(absolute_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def auth(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    signup_form = SignupForm()
    signin_form = LoginForm()
    context = {
        "signup_form": signup_form,
        "signin_form": signin_form,
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "auth.html", context)

@login_required(login_url="auth")
def dashboard(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "dashboard.html", context)

def home(request):
    faq_data = load_json_file('app/faq_data/home.json')
    context = {
        "faq_data": faq_data,
        "header_color": "background-color: rgb(64, 135, 177) !important"
    }
    return render(request, 'home.html', context)

def works(request):
    faq_data_1 = load_json_file('app/faq_data/works/general.json')
    faq_data_2 = load_json_file('app/faq_data/works/buying.json')
    faq_data_3 = load_json_file('app/faq_data/works/selling.json')
    context = {
        "faq_data_1": faq_data_1,
        "faq_data_2": faq_data_2,
        "faq_data_3": faq_data_3,
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "works.html", context)

def buy(request):
    faq_data = load_json_file('app/faq_data/buy.json')
    context = {
        "faq_data": faq_data,
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "buy.html", context)

def sell(request):
    faq_data = load_json_file('app/faq_data/sell.json')
    context = {
        "faq_data": faq_data,
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "sell.html", context)

def blog(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, 'blog.html', context)

def contact(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "contact.html", context)

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)  
                return redirect('dashboard') 
            else:
                form.add_error(None, "Invalid username or password.")
        else:
            form.add_error(None, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'auth.html', {
        "signin_form": form,
        "signup_form": SignupForm(),  
    })

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                auth_login(request, user)  
                return redirect('dashboard')
        else:
            return render(request, 'auth.html', {
                "signup_form": form,
                "signin_form": LoginForm(),
            })

    return render(request, 'auth.html', {
        "signup_form": SignupForm(),
        "signin_form": LoginForm(),
    })
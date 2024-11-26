from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm
from django.contrib.auth.forms import UserCreationForm


def auth(request):
    signup_form = SignupForm()
    signin_form = LoginForm()
    return render(request, "auth.html", {"signup_form": signup_form, "signin_form":signin_form })

def home(request):
    context = {
        "header_color": "background-color: rgb(64, 135, 177) !important"
    }
    return render(request, 'home.html', context)

def works(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "works.html", context)

def buy(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "buy.html", context)

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)  # Log the user in
                return redirect('home')  # Redirect to home on success
            else:
                # Add error for invalid credentials
                form.add_error(None, "Invalid username or password.")
        else:
            # Form validation errors will be shown automatically
            form.add_error(None, "Please correct the errors below.")
    else:
        form = LoginForm()

    # Render the login page with the login form and any errors
    return render(request, 'auth.html', {
        "signin_form": form,
        "signup_form": SignupForm(),  # Include signup form for rendering the same page
    })

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                auth_login(request, user)  # Automatically log the user in
                return redirect('home')
        else:
            # Render the form with validation errors
            return render(request, 'auth.html', {
                "signup_form": form,
                "signin_form": LoginForm(),
            })

    # Render a blank form for GET requests
    return render(request, 'auth.html', {
        "signup_form": SignupForm(),
        "signin_form": LoginForm(),
    })
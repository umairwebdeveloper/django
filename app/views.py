from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from .utils import load_json_file, send_email
from .forms import LoginForm, StartUserForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Transaction, Vehicle
from .forms import UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseForbidden


def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    errors = None
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user: 
                auth_login(request, user)  
                return redirect('dashboard') 
            else:
                form.add_error(None, "Invalid email or password")
            
    context = {
        "signin_form": form,
        "errors": form.errors if form.errors else errors,
        "header_color": "background-color: rgb(26, 43, 99) !important",
    }
    
    return render(request, "login.html", context)


def register(request, transaction_id):
    if request.user.is_authenticated:
        return redirect("dashboard")
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    transaction_email = transaction.user.email
    user_instance = transaction.user  # Get the user instance from the transaction

    if not transaction_email:
        raise Http404("Associated email not found for the transaction.")

    errors = None
    if request.method == 'POST':
        form = StartUserForm(request.POST, user_instance=user_instance)
        if form.is_valid():
            try:
                user = form.save()
                password = form.cleaned_data['password']
                # Automatically log in the user
                auth_login(request, user)

                messages.success(request, "User registered and logged in successfully.")
                subject = 'Welcome to KeySavvy! We are your partner in private party vehicle sales.'
                recipient_list = [user.email]
                template_path = 'emails/wellcome.html'
                context = {
                    "user_email": user.email,
                    "user_password": password,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                send_email(subject, recipient_list, template_path, context)
                return HttpResponseRedirect(f"{reverse('dashboard')}?from_signup=true")
            except Exception as e:
                messages.error(request, f"Error saving form: {str(e)}")
        else:
            errors = form.errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = StartUserForm(user_instance=user_instance)

    context = {
        "signup_form": form,
        "errors": errors,
        "header_color": "background-color: rgb(26, 43, 99) !important",
    }
    return render(request, "register.html", context)


@login_required(login_url="auth")
def dashboard(request):
    user = request.user
    try:
        profile = request.user.profile
        profile_status = profile.status
    except UserProfile.DoesNotExist:
        profile_status = "pending"
    
    # Retrieve the latest non-canceled transaction for the user
    transaction = Transaction.objects.filter(user=user).last()
    vehicle = transaction.vehicle if transaction else None
    transaction_id = transaction.transaction_id if transaction else None
    transaction_cancel = transaction.cancel if transaction else None
    
    context = {
        "user": user,
        "vehicle": vehicle,
        "transaction_id": transaction_id,
        "dashboard": True,
        "from_signup": None,
        "profile_status": profile_status, 
        "transaction_cancel": transaction_cancel,
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

def trust(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, 'trust.html', context)

def contact(request):
    context = {
        "header_color": "background-color: rgb(26, 43, 99) !important"
    }
    return render(request, "contact.html", context)

@login_required(login_url="auth")
def add_or_update_profile(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
        
    try:
        u_profile = request.user.profile
        profile_status = u_profile.status
    except UserProfile.DoesNotExist:
        profile_status = "pending"

    return render(request, 'profile.html', {'form': form, "profile_status": profile_status, "header_color": "background-color: rgb(26, 43, 99) !important"})


def verify_transaction(request, transaction_id):
    """
        view to verify the serial number and email from the unique link.
    """
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    faq_data = load_json_file('app/faq_data/sell.json')
    
    context = {
        "transaction": transaction,    
        "faq_data": faq_data,
        "header_color": "background-color: rgb(26, 43, 99) !important"
     }

    if request.method == "POST":
        entered_serial = request.POST.get("serial_number")
        if entered_serial == transaction.vehicle.serial_number:
            transaction.cancel = False
            transaction.save()
            return redirect(f"/details/{transaction.transaction_id}/")
        else:
            context["error"] = "*Invalid VIN entered"
            return render(request, "verify_transaction.html", context)
    
    return render(request, "verify_transaction.html", context)


def vehicle_details(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    if request.user.is_authenticated:
        return redirect("dashboard")

    # if request.method == "POST":
    #     # Create user and send email
    #     user = transaction.user
    #     new_password = generate_secure_password(length=8)
    #     user.set_password(new_password)  # generated password
    #     user.save()
    #     subject = 'Welcome to KeySavvy! We are your partner in private party vehicle sales.'
    #     recipient_list = [user.email]
    #     template_path = 'emails/wellcome.html'
    #     context = {
    #         "user_email": user.email,
    #         "user_name": user.username,
    #         "user_password": new_password, 
    #         "first_name":user.first_name,
    #         "last_name": user.last_name
    #     }
    #     # send_email(subject, recipient_list, template_path, context) 

    #     return redirect("auth")

    return render(request, "vehicle_details.html", {"transaction": transaction, "header_color": "background-color: rgb(26, 43, 99) !important"})


@login_required
def update_phone_number(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        phone_number = request.POST.get("phone_number", user.phone_number.number)
        user.phone_number.number = phone_number
        user.phone_number.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@login_required
def cancel_transaction(request, transaction_id):
    if request.method == "POST":
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id, user=request.user)
        if transaction.cancel:
            return HttpResponseForbidden("Transaction already canceled.")
        transaction.cancel = True
        transaction.save()
        return redirect('dashboard')
    return HttpResponseForbidden("Invalid request method.")
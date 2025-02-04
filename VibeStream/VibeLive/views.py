from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = {}

        # Check if passwords match
        if password1 != password2:
            errors['password2'] = "Passwords do not match"

        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            errors['email'] = "Email is already registered."

        # Create the user
        if not errors:
            try:
                user = User.objects.create_user(username=email, email=email, password=password1)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                # Optionally, auto-login the user after registration
                login(request, user)

                return redirect('login')  # Redirect to login page after successful registration

            except Exception as e:
                errors['general'] = str(e)

        # If there are errors, return the form with error messages
        return render(request, 'register.html', {
            'error_first_name': errors.get('first_name', ''),
            'error_last_name': errors.get('last_name', ''),
            'error_email': errors.get('email', ''),
            'error_password1': errors.get('password1', ''),
            'error_password2': errors.get('password2', ''),
            'messages': messages.get_messages(request),
            'error_general': errors.get('general', '')
        })

    return render(request, 'register.html')


def signin(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')

@login_required
def dashboard(request):
    context = {
        'name': request.user.first_name
    }
    print(context)
    return render(request, 'dashboard.html', context)

@login_required
def meeting(request):
    context = {
        'name': request.user.first_name + " " + request.user.last_name
    }
    return render(request, 'meeting.html', context)

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect("/signin")
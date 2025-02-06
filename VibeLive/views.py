from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'index.html', {'tittle': 'Home'})

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

                # Send email on account creation
                send_mail(
                    'Welcome to VibeStream',  # Subject
                    f'Hello {user.first_name},\n\n'
                    f'Welcome to VibeStream! We are thrilled to have you as part of our community.\n\n'
                    f'With VibeStream, you can connect, collaborate, and share amazing moments seamlessly. We strive to provide the best experience for you, and our support team is always here if you need any help.\n\n'
                    f'If you have any questions, feel free to reach out to us anytime.\n\n'
                    f'Enjoy your journey with VibeStream!\n\n'
                    f'Best regards,\n'
                    f'Saumili Haldar\n'
                    f'VibeStream Team',  # Message body
                    settings.EMAIL_HOST_USER,  # From email
                    [user.email],  # To email
                    fail_silently=False,
                )


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

    return render(request, 'register.html', {'tittle': 'SignUp'})


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

    return render(request, 'login.html', {'tittle': 'Login'})

@login_required
def dashboard(request):
    context = {
        'name': request.user.first_name,
        'tittle': 'Dashboard'
    }
    print(context)
    return render(request, 'dashboard.html', context)

@login_required
def meeting(request):
    context = {
        'name': request.user.first_name + " " + request.user.last_name
        , 'tittle': 'Meeting'
    }
    return render(request, 'meeting.html', context)

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html',  {'tittle': 'Join Room'})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/signin")
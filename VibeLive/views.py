from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.signing import Signer, BadSignature
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse

signer = Signer()

def index(request):
    return render(request, 'index.html', {'tittle': 'Home'})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Use a different email.")
            return redirect('register')

        try:
            # Create a new inactive user
            user = User.objects.create_user(username=email, email=email, password=password1)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False  # User will be activated after email verification
            user.save()

            # Generate verification token
            token = signer.sign(email)
            uid = urlsafe_base64_encode(force_bytes(email))
            
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
            )

            send_mail(
                'Verify Your Email - VibeStream',
                f'Hello {first_name},\n\n'
                f'Please verify your email by clicking the link below:\n\n'
                f'{verification_link}\n\n'
                f'Best Regards,\n'
                f'Saumili Haldar\nVibeStream Team',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return render(request, 'register.html', {'email_sent': True})

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'register.html', {'tittle': 'SignUp'})

def verify_email(request, uidb64, token):
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        original_email = signer.unsign(token)

        if email == original_email:
            try:
                user = User.objects.get(email=email)
                user.is_active = True  # Activate user after verification
                user.save()
                return render(request, 'register.html', {'email_verified': True})
            except User.DoesNotExist:
                return HttpResponse("User not found.", status=404)

        return HttpResponse("Invalid verification link.", status=400)

    except (BadSignature, ValueError, TypeError):
        return HttpResponse("Invalid or expired verification link.", status=400)

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Get user by email
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username
            
            if user is not None:
                login(request, user)
                print("Login successful. Redirecting to /dashboard...")  # Debugging
                return redirect('/dashboard')  # Ensure redirect is properly set
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')

    return render(request, 'login.html', {'tittle': 'Login'})

@login_required
def dashboard(request):
    context = {
        'name': request.user.first_name,
        'tittle': 'Dashboard'
    }
    return render(request, 'dashboard.html', context)

@login_required
def meeting(request):
    context = {
        'name': f"{request.user.first_name} {request.user.last_name}",
        'tittle': 'Meeting'
    }
    return render(request, 'meeting.html', context)

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect(f"/meeting?roomID={roomID}")
    return render(request, 'joinroom.html', {'tittle': 'Join Room'})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/signin")

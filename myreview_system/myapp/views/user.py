import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def home(request):
    # Example of rendering an HTML template
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Please provide both email and password.'}, status=400)

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # Secure password check
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to 'home' view
            else:
                return JsonResponse({"error": "Incorrect password"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return render(request, 'login.html')


def user_signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST.get('username', email)  # Use email as default username

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'signup.html')


def user_logout(request):
    logout(request)
    return redirect('login')



# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         # Ensure email field is not empty
#         if not email:
#             messages.error(request, 'Email field cannot be empty.')
#             return redirect('forgot_password')

#         # Check if the email exists
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             messages.error(request, 'Email not registered.')
#             return redirect('forgot_password')

#         # Generate OTP
#         otp = random.randint(100000, 999999)

#         # Save OTP in session
#         request.session['otp'] = otp
#         request.session['email'] = email

#         try:
#             # Send OTP to user's email
#             send_otp_email(email, otp)
#             messages.success(request, 'OTP sent to your email.')
#         except Exception as e:
#             messages.error(request, f'Failed to send OTP: {e}')

#         return redirect('otp_verification')  # Redirect to OTP verification page

#     return render(request, 'forgot_password.html')

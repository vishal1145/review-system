from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password
import random
import string


# Generate OTP
def generate_otp():
    """Generate a random OTP."""
    return ''.join(random.choices(string.digits, k=6))


# Send OTP via email
def send_otp_email(email, otp):
    """Send OTP to the user's email."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
    except Exception as e:
        print(f"Error sending OTP email: {e}")


# Forgot Password View
def forgot_password(request):
    """View for handling forgot password logic."""
    if request.method == 'POST':
        email = request.POST.get('email')

        # Ensure email field is not empty
        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('forgot_password')

        # Check if the email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email not registered.')
            return redirect('forgot_password')

        # Generate OTP
        otp = generate_otp()

        # Save OTP and email in session
        request.session['otp'] = otp
        request.session['email'] = email

        try:
            # Send OTP to user's email
            send_otp_email(email, otp)
            messages.success(request, 'OTP sent to your email.')
        except Exception as e:
            messages.error(request, f'Failed to send OTP: {e}')

        return redirect('otp')  # Redirect to OTP verification page

    return render(request, 'forgot_password.html')


def otp_verification(request):
    """View to verify OTP and proceed to reset password."""
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        # Retrieve OTP and email from session
        stored_otp = request.session.get('otp')
        email = request.session.get('email')

        # Verify OTP
        if entered_otp == stored_otp:
            # OTP is correct, proceed to reset password page
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('otp')

    return render(request, 'otp_verification.html')

def reset_password(request):
    """View for resetting the password after OTP verification."""
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

        # Get the user's email from session and update password
        email = request.session.get('email')
        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful. You can now log in.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('forgot_password')

    return render(request, 'reset_password.html')

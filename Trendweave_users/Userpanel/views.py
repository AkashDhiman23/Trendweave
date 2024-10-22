from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from .forms import CustomUserRegisterForm
from .models import CustomUser

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = CustomUser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']  # Store password in plain text for testing
            )
            user.generate_otp()  # Generate OTP
            user.save()
            
            try:
                # Send OTP to the user's email
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is: {user.otp}',
                    'trendweavenz@outlook.com',  # Your office email address
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Registration successful! Check your email for the OTP.')
                return redirect('users:verify_otp', username=user.username)  # Redirect to OTP verification page
            
            except Exception as e:
                messages.error(request, f'Error sending email: {e}')
                return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserRegisterForm()

    return render(request, 'register.html', {'form': form})

def verify_otp(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('users:register')  # Redirect to registration page if user not found

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if user.otp == entered_otp:
            messages.success(request, 'OTP verified successfully! You can log in now.')
            return redirect('users:login')  # Redirect to login page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'verify_otp.html', {'username': username})

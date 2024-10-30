from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login# type: ignore
from django.shortcuts import render, redirect# type: ignore
from django.contrib import messages# type: ignore
from .forms import CustomUserForm , LoginForm # Ensure you have a form class for user registration

# Create your views here.
def index(request):
    return render(request, 'index.html')



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"Attempting to log in with Email: {email}")  # Debug print

            # Authenticate using email if your user model uses email as the username
            user = authenticate(request, username=email, password=password)
            print(f"Authenticated User: {user}")  # Debug print

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                print("Login successful, redirecting to index")  # Debug print
                return redirect('index')  # Make sure 'index' is the correct URL name
            else:
                messages.error(request, 'Invalid email or password.')
                print("Login failed: Invalid email or password.")  # Debug print
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)  # Use the form class for validation
        if form.is_valid():
            # Create a new user instance without hashing the password
            user = CustomUser(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password']  # Save password in plain text
            )
            user.save()  # Save the user instance
            
            messages.success(request, 'Registration successful! You can log in now.')
            return render(request, 'login.html', {'form': form})  # Redirect to the login page
    else:
        form = CustomUserForm()  # Create an empty form instance for GET requests

    return render(request, 'register.html', {'form': form})


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')



def contact(request):
    return render(request, 'contact.html')





def shop(request):
    return render(request, 'shop.html')






from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import AdminRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import AdminRegister


def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Debugging output
        print(f"Attempting to log in with email: {email}")

        user = authenticate(request, email=email, password=password)  # Assuming email as username
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your admin dashboard
        else:
            messages.error(request, "Invalid credentials")
            print("Invalid login attempt")  # Debugging output

    return render(request, 'index.html')


def registration_view(request):

    if request.method == 'POST':
        form = AdminRegisterForm(request.POST) 
        if form.is_valid():
            form.save()  
            return redirect('dashboard')  
    else:
        form = AdminRegisterForm()  

    return render(request, 'registration.html', {'form': form})

def logout_view(request):
    logout(request)  
    return redirect('index')

def dashboard(request):
    # Check if the admin is logged in
    if 'admin_id' in request.session:
        return render(request, 'dashboard.html')
    else:
        return redirect('index') 


from django.http import HttpResponse # type: ignore
from django.shortcuts import render, redirect # type: ignore
from .forms import AdminRegisterForm
from django.contrib.auth import authenticate, login,logout # type: ignore
from django.contrib import messages # type: ignore
from .models import AdminRegister


def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Debugging output
        print(f"Attempting to log in with email: {email}")

        try:
            # Look for the user with the entered email
            user = AdminRegister.objects.get(email=email)

            # Check if the password matches (since it's stored in plain text)
            if user.password == password:
                # Set the session to keep the user logged in
                request.session['admin_id'] = user.admin_id
                return redirect('dashboard')  # Redirect to the admin dashboard
            else:
                messages.error(request, "Invalid password")
                print("Invalid password")  # Debugging output

        except AdminRegister.DoesNotExist:
            messages.error(request, "Invalid email")
            print("Invalid email")  # Debugging output

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
    

def profile_view(request):
    # Fetch the logged-in admin's ID from the session
    admin_id = request.session.get('admin_id')

    if not admin_id:
        return redirect('index')  # Redirect to login if no admin is logged in

    try:
        # Get the logged-in admin's data
        admin = AdminRegister.objects.get(admin_id=admin_id)
    except AdminRegister.DoesNotExist:
        return redirect('index')  # Handle case where admin does not exist

    # Pass the admin's data to the template
    context = {
        'admin': admin
    }

    return render(request, 'profile.html', context)


def category_view(request):
    return render(request, 'category.html')


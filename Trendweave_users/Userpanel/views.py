from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login# type: ignore
from django.shortcuts import render, redirect# type: ignore
from django.contrib import messages# type: ignore

from .forms import CustomUserForm 

def index(request):
    from admin_panel.models import Category, Subcategory, Product  # Move import here
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    
    return render(request, 'index.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)  # Query the user by email
            if user.password == password:  # Direct password comparison
                request.session['user_id'] = user.customuser_id
                return redirect('shop')  # Redirect to a success page
            else:
                messages.error(request, "Invalid password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "No user with this email exists.")
    
    return render(request, 'login.html')



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

    return render(request, 'registeration.html', {'form': form})


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')



def contact(request):
    return render(request, 'contact.html')





def shop(request):
    from admin_panel.models import Category, Subcategory, Product  
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    
    return render(request, 'shop.html', context)







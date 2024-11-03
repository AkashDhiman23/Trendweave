from urllib import request
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from .models import CustomUser, Cart
from django.contrib.auth import authenticate, login as auth_login # type: ignore
from django.contrib.auth.models import User,auth # type: ignore
from .forms import CustomUserForm , LoginForm # Ensure you have a form class for user registration
from django.contrib.auth.decorators import login_required # type: ignore



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)  
            if user.password == password:  # Compare directly with plain-text password
                request.session['user_id'] = user.customuser_id  # Save user ID in session
                return redirect('shop') 
            else:
                messages.error(request, "Invalid password.")
        except CustomUser.DoesNotExist:
            messages.error(request, "No user with this email exists.")
    
    return render(request, 'login.html')


def logout(request):
    request.session.flush()  # Clear all session data
    messages.success(request, "You have been logged out.")
    return redirect('login')



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

# Create your views here.
def checkout(request):
    return render(request, 'checkout.html')



def contact(request):
    return render(request, 'contact.html')



@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})





    
def search(request):
    from admin_panel.models import Category, Subcategory, Product 
    query = request.GET.get('query')  # This gets the 'query' parameter from the URL
    data = Product.objects.filter(name__icontains=query) 
    return render(request, 'search.html', {'data': data, 'query': query})


def shop(request):
    from admin_panel.models import Category, Subcategory, Product  # Move import here
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    
    return render(request, 'shop.html', context)



def product(request, product_id):
    from admin_panel.models import Category, Subcategory, Product  # Move import here
    product = get_object_or_404(Product, product_id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def add_cart(request,product_id):
    from admin_panel.models import Category, Subcategory, Product  # Move import here
    product = get_object_or_404(Product, product_id=product_id)
    # if cart.objects.filter(u_id=request.user,p_id=p).exists():
    #     messages.warning(request,'Product is already exists...')
    #     return redirect('/cart/')
    # else:
    #     c = Cart(p_id=p,u_id=request.user,quantity=1)
    #     c.save()
    messages.success(request,'Product is added to the Cart...')
    return redirect('/cart/')





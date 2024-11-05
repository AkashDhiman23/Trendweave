from urllib import request
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from django.contrib.auth.decorators import login_required
from .models import CustomUser ,Wish, Cart
from django.contrib.auth import authenticate, login 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .forms import CustomUserForm , LoginForm # Ensure you have a form class for user registration
from django.http import JsonResponse


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Debugging output (remove in production)
        print(f"Trying to log in user with email: {email}")
        
        # Authenticate the user
        user = auth.authenticate(request, email=email, password=password)
        
        if user is not None:
            # Log the user in
            auth.login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('/shop/')
        else:
            messages.warning(request, 'Invalid credentials. Please try again.')
            return redirect('/login/')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Collect email
        first_name = request.POST.get('first_name')  # Collect first name
        last_name = request.POST.get('last_name')  # Collect last name
        password = request.POST.get('password')  # Collect password

        # Ensure that all required fields are provided
        if email and first_name and last_name and password:
            # Create a new user instance without hashing the password
            user = CustomUser(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password  # Save password in plain text
            )
            user.save()  # Save the user instance

            messages.success(request, 'Registration successful! You can log in now.')
            return redirect('login') 
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'registeration.html') 



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



def cart(request):
    return render(request, 'cart.html')



    
def search(request):
    from admin_panel.models import Category, Subcategory, Product 
    query = request.GET.get('query')  # This gets the 'query' parameter from the URL
    data = Product.objects.filter(name__icontains=query)  # Change pname to name
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



@login_required
def add_cart(request, product_id):
    from admin_panel.models import Product
    product = get_object_or_404(Product, product_id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        customuser=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if created:
        message = 'Product added to the cart.'
    else:
        cart_item.quantity += 1
        cart_item.save()
        message = 'Product quantity updated in your cart.'

    return JsonResponse({'success': True, 'message': message})



def logout(request):
    # Clear the user ID from the session
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "You have successfully logged out.")
    
 
    return redirect('index') 

@login_required
def wishlist_count(request):
    # Count the total number of products in the user's wishlist
    wishlist_count = Wish.objects.filter(customuser=request.user).count()
    return {'wishlist_count': wishlist_count}



def wish(request):
    # Filter the wishlist items for the currently authenticated user
    data = Wish.objects.select_related('product').filter(customuser=request.user)  # Ensure this is the correct field name

    g_total = 0
    for d in data:
        g_total += d.sub_total()  # Assuming this method calculates the subtotal for each item

    # Render the wishlist template with the wishlist data and grand total
    return render(request, 'wishlist.html', {'data': data, 'g_total': g_total})


def add_wish(request, pid):
    # Get the product instance using the product_id
    from admin_panel.models import Product
    product = get_object_or_404(Product, product_id=pid)

    # Check if the product is already in the wishlist
    wishlist_item, created = Wish.objects.get_or_create(
        customuser=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if created:
        messages.success(request, 'Product added to your wishlist!')
    else:
        # If the item already exists, increment the quantity
        wishlist_item.quantity += 1
        wishlist_item.save()
        messages.info(request, 'Product quantity updated in your wishlist!')

    return redirect('/wish/')

@login_required(login_url='/login/')
def profile(request):
    # Fetch the logged-in admin's ID from the session
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('index')  # Redirect to login if no admin is logged in

    try:
        # Get the logged-in admin's data
        customUser = CustomUser.objects.get(customuser_id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('index')  # Handle case where admin does not exist

    # Pass the admin's data to the template
    context = {
        'customUser': customUser  # Use 'customUser' instead of 'user'
    }

    return render(request, 'myprofile.html', context)

@login_required(login_url='/login/')
def cart_view(request):
    # Get all cart items for the current user
    cart_items = Cart.objects.filter(CustomUser=request.user)

    # Calculate subtotal for each item and the grand total
    grand_total = 0
    for item in cart_items:
        item.sub_total = item.product.price * item.quantity
        grand_total += item.sub_total

    # Pass cart data to template
    context = {
        'data': cart_items,
        'g_total': grand_total,
    }
    return render(request, 'cart.html', context)

def filter_products(request):
    prices = request.GET.getlist('prices[]')  # Adjust to match how data is sent
    sizes = request.GET.getlist('sizes[]')

    # Build your query based on the received filters
    from admin_panel.models import Product
    products = Product.objects.all()

    if prices:
        products = products.filter(price__in=prices)
    if sizes:
        products = products.filter(size__in=sizes)

    product_list = [{'product_id': product.id, 'name': product.name, 'price': product.price, 'image_1': product.image_1.url} for product in products]

    return JsonResponse({'products': product_list})
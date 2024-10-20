from django.http import HttpResponse, JsonResponse # type: ignore
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from .forms import AdminRegisterForm
from django.contrib.auth import authenticate, login,logout # type: ignore
from django.contrib import messages # type: ignore
from .models import AdminRegister,Category, Subcategory, Product
from django.utils.text import slugify # type: ignore
from django.http import JsonResponse# type: ignore
from django.views.decorators.csrf import csrf_exempt# type: ignore


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


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})


def add_category(request):
    if request.method == 'POST':
        # Get the category name and description from the form data
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        # Generate the slug from the category name
        category_slug = slugify(category_name)

        # Check if the category with the same slug already exists
        if Category.objects.filter(slug=category_slug).exists():
            return JsonResponse({'status': 'error', 'message': 'A category with this slug already exists.'})

        # Get the admin instance using the admin_id from the session
        admin_id = request.session.get('admin_id')
        try:
            admin = AdminRegister.objects.get(admin_id=admin_id)
        except AdminRegister.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Admin not found.'})

        # Create and save the new category instance with the admin instance
        category = Category(
            name=category_name,
            slug=category_slug,
            description=category_description,
            admin_id=admin  # Assign the AdminRegister instance here
        )
        category.save()

        return JsonResponse({'status': 'success', 'message': 'Category added successfully.'})

    return render(request, 'category.html')




def add_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        subcategory_name = request.POST.get('subcategory_name')
        subcategory_description = request.POST.get('subcategory_description', '')
        
        # Get the admin_id from the session
        admin_id = request.session.get('admin_id')

        # Debug: Print out the values received
        print(f"Category ID: {category_id}, Subcategory Name: {subcategory_name}, Description: {subcategory_description}, Admin ID: {admin_id}")

        # Retrieve the AdminRegister instance
        admin_instance = get_object_or_404(AdminRegister, admin_id=admin_id)

        # Check if the subcategory already exists
        if Subcategory.objects.filter(name=subcategory_name).exists():
            messages.error(request, "Subcategory with this name already exists.")
            return redirect('subcategory_view')

        # Create the subcategory
        subcategory = Subcategory.objects.create(
            category_id=category_id,
            name=subcategory_name,
            description=subcategory_description,
            admin_id=admin_instance  # Use the AdminRegister instance instead of admin_id
        )
        messages.success(request, "Subcategory added successfully.")
        return redirect('subcategory_view')

    categories = Category.objects.all()
    return render(request, 'subcategory.html', {'categories': categories})






def subcategory_view(request):
    # categories = Category.objects.all()
    categories = Category.objects.all()
    return render(request, 'subcateogory.html', {'categories': categories})




def product(request):
    products = Product.objects.all()  # Fetch all products
    categories = Category.objects.all()  # Fetch all categories (if needed)
    subcategory= Subcategory.objects.all()
    return render(request, 'product.html', {
        'product': products,
        'categories': categories,
        'subcategory':subcategory,
    })






def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')
        image_3 = request.FILES.get('image_3')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

           # Get the admin_id from the session
        admin_id = request.session.get('admin_id')

        # Debugging: Print the values received
        print(f"Category ID: {category_id}, Subcategory ID: {subcategory_id}")

          # Retrieve the AdminRegister instance
        admin_instance = get_object_or_404(AdminRegister, admin_id=admin_id)


        # Validate that category_id is not empty
        if not category_id:
            return render(request, 'product.html', {'error': 'Category is required', 'categories': Category.objects.all(), 'subcategories': Subcategory.objects.all()})

        # Validate that the category exists
        if not Category.objects.filter(pk=category_id).exists():
            return render(request, 'product.html', {'error': 'Invalid category selected', 'categories': Category.objects.all(), 'subcategories': Subcategory.objects.all()})

        # Validate that the subcategory exists
        if not Subcategory.objects.filter(pk=subcategory_id).exists():
            return render(request, 'product.html', {'error': 'Invalid subcategory selected', 'categories': Category.objects.all(), 'subcategories': Subcategory.objects.all()})

        # Create and save the product instance
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            admin_id=admin_instance,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3,
            category_id=category_id,
            subcategory_id=subcategory_id,
        )
        product.save()  # Save the product instance to the database
        return redirect('product')  # Change this to your redirect view

    # Retrieve categories and subcategories to display in the form
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    return render(request, 'product.html', {'categories': categories, 'subcategories': subcategories})



def edit_product(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.category_id = request.POST.get('category')
        product.subcategory_id = request.POST.get('subcategory')

        # Handle image uploads if necessary
        if 'image_1' in request.FILES:
            product.image_1 = request.FILES['image_1']
        if 'image_2' in request.FILES:
            product.image_2 = request.FILES['image_2']
        if 'image_3' in request.FILES:
            product.image_3 = request.FILES['image_3']

        product.save()
        return redirect('product.html')  # Redirect to the product list page
    


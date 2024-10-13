from django.http import HttpResponse, JsonResponse # type: ignore
from django.shortcuts import render, redirect # type: ignore
from .forms import AdminRegisterForm
from django.contrib.auth import authenticate, login,logout # type: ignore
from django.contrib import messages # type: ignore
from .models import AdminRegister,Category, Subcategory, Product
from django.utils.text import slugify # type: ignore


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

        # Create and save the new category instance
        category = Category(
            name=category_name,
            slug=category_slug,
            description=category_description,
            admin_id=admin  # Assign the AdminRegister instance here
        )
        category.save()

        

    return render(request, 'category.html')




def add_subcategory(request):
    if request.method == 'POST':
        # Get the subcategory name, description, and category ID from the form data
        subcategory_name = request.POST.get('subcategory_name')
        subcategory_description = request.POST.get('subcategory_description')
        category_id = request.POST.get('category_id')  # Assuming you're getting the category ID

        # Check if the subcategory with the same name already exists
        if Subcategory.objects.filter(name=subcategory_name).exists():
            return JsonResponse({'status': 'error', 'message': 'A subcategory with this name already exists.'})

        # Get the admin instance using the admin_id from the session
        admin_id = request.session.get('admin_id')
        try:
            admin = AdminRegister.objects.get(id=admin_id)  # Use 'id' instead of 'admin_id'
        except AdminRegister.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Admin not found.'})

        # Get the category instance to link with the subcategory
        try:
            # Use the id field directly for the ForeignKey
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Category not found.'})

        # Create and save the new subcategory instance
        subcategory = Subcategory(
            name=subcategory_name,
            description=subcategory_description,
            admin_id=admin,  # Assign the AdminRegister instance here
            category_id=category  # Link to the selected category
        )
        subcategory.save()

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'Subcategory added successfully.'})

    return render(request, 'subcategory.html')









def subcategory_view(request):
    # categories = Category.objects.all()
    categories = Category.objects.all()
    return render(request, 'subcateogory.html', {'categories': categories})



def product(request):
    # product=Product.object.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()  # Corrected variable name for consistency
    context = {
        'categories': categories,
        'subcategories': subcategories,
      
    }
    return render(request, 'product.html', context)








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

        # Debugging: Print the values received
        print(f"Category ID: {category_id}, Subcategory ID: {subcategory_id}")

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


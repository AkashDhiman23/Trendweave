from django.http import HttpResponse, JsonResponse 
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AdminRegisterForm
from django.contrib.auth import authenticate, login,logout 
from django.contrib import messages 
from .models import AdminRegister,Category, Subcategory, Product
from django.utils.text import slugify 



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
                # request.session['first_name']
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
    from Userpanel.models import Order,OrderItem,CustomUser
    if 'admin_id' in request.session:
        # Fetch counts from the database
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        subcategory_count = Subcategory.objects.count()

       
    user_count = CustomUser.objects.count()  # Adjust this if you're using a custom user model
    order_count = Order.objects.count()  # Adjust this if you have an Order model

  
        # Prepare context data to send to the template
    context = {
            'product_count': product_count,
            'category_count': category_count,
            'subcategory_count': subcategory_count,
            'user_count': user_count,
        'order_count': order_count,
    }
        
    return render(request, 'dashboard.html', context)



def edit_product(request):
    if request.method == "POST":
        # Retrieve product ID from the form
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        # Update product details
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.size = request.POST.get('size')  
       
      

        # Save the updated product details to the database
        product.save()

        
        return redirect('product')

    elif request.method == "GET":
        # Retrieve product ID from the query parameters
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()

        # Render the template with the product details and lists of categories/subcategories
        return render(request, 'product.html', {
            'product': product,
            'categories': categories,
            'subcategories': subcategories
        })










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
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})



def add_category(request):
    if request.method == 'POST':
        # Get the category name and description from the form data
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        # Check if the category name is provided
        if not category_name:
            return JsonResponse({'status': 'error', 'message': 'Category name is required.'})

        # Generate the slug from the category name
        category_slug = slugify(category_name)

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

        # Redirect to the category list or another appropriate view
        return render(request, 'category.html')

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


def user_view(request):
    from Userpanel.models import CustomUser
    # categories = Category.objects.all()
    CustomUser = CustomUser.objects.all()
    return render(request, 'user.html', {'CustomUser': CustomUser})




def delete_subcategory(request, subcategory_id):
    # Ensure the request method is POST to prevent accidental deletions
    if request.method == 'POST':
        # Retrieve the subcategory instance to be deleted
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)

        # Delete the subcategory
        subcategory.delete()
        
        # Set a success message
        messages.success(request, "Subcategory deleted successfully.")
        return redirect('subcategory_view')

    # If the request is not POST, redirect back to the subcategory view
    messages.error(request, "Invalid request.")
    return redirect('subcategory_view')




def product(request):
    products = Product.objects.all()  # Fetch all products
    categories = Category.objects.all()  # Fetch all categories (if needed)
    subcategory = Subcategory.objects.all()  # Fetch all subcategories
    return render(request, 'product.html', {
        'product': products,
        'categories': categories,
        'subcategory': subcategory,
    })



def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        size = request.POST.get('size')  # Get size from the form
        image_1 = request.FILES.get('image_1')
        image_2 = request.FILES.get('image_2')
        image_3 = request.FILES.get('image_3')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

        # Get the admin_id from the session
        admin_id = request.session.get('admin_id')

        # Debugging: Print the values received
        print(f"Category ID: {category_id}, Subcategory ID: {subcategory_id}, Size: {size}")

        # Retrieve the AdminRegister instance
        admin_instance = get_object_or_404(AdminRegister, admin_id=admin_id)

        # Validate that category_id is not empty
        if not category_id:
            return render(request, 'product.html', {
                'error': 'Category is required',
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.all()
            })

        # Validate that the category exists
        if not Category.objects.filter(pk=category_id).exists():
            return render(request, 'product.html', {
                'error': 'Invalid category selected',
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.all()
            })

        # Validate that the subcategory exists
        if not Subcategory.objects.filter(pk=subcategory_id).exists():
            return render(request, 'product.html', {
                'error': 'Invalid subcategory selected',
                'categories': Category.objects.all(),
                'subcategories': Subcategory.objects.all()
            })

        # Create and save the product instance
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            size=size, 
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
    return render(request, 'product.html', {
        'categories': categories,
        'subcategories': subcategories
    })


def edit_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')  # Get category ID from the POST request
        category_name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        category_description = request.POST.get('category_description')

        # Retrieve the category to be edited using the correct field name
        category = get_object_or_404(Category, category_id=category_id)

        # Update the category's details
        category.name = category_name
        category.slug = slug
        category.description = category_description
        category.save()

        messages.success(request, 'Category updated successfully!')
        return redirect('category')  # Redirect to your category list view

    return redirect('category') 



def edit_subcategory(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory_id')
        subcategory_name = request.POST.get('subcategory_name')
        subcategory_description = request.POST.get('subcategory_description')

        # Retrieve the subcategory to be edited
        subcategory = get_object_or_404(Subcategory, subcategory_id=subcategory_id)

        # Update the subcategory's details
        subcategory.name = subcategory_name
        subcategory.description = subcategory_description
        subcategory.save()

        messages.success(request, 'Subcategory updated successfully!')
        return redirect('subcategory_view')  # Redirect to your subcategory list view

    return redirect('subcategory_view')  # Redirect if not a POST request


def delete_subcategory(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory_id')

        # Retrieve the subcategory to be deleted
        subcategory = get_object_or_404(Subcategory, subcategory_id=subcategory_id)
        subcategory.delete()

        messages.success(request, 'Subcategory deleted successfully!')
        return redirect('subcategory_view') 

    return redirect('subcategory_view')  



def delete_category(request, category_id):
  
    category = get_object_or_404(Category, category_id=category_id)
    
    if request.method == "POST":
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" was deleted successfully.')
        return redirect('category')  # Redirect to the category management page

    return render(request, 'category.html', {'categories': Category.objects.all()})






def order_view(request):
    from Userpanel.models import Order,OrderItem
    # Product=Product.objects.all()
    OrderItem=OrderItem.objects.all()
    Order = Order.objects.all()

    return render(request, 'order.html', {'Order': Order})



def update_order_status(request):
    from Userpanel.models import Order
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        print(f"Received order_id: {order_id}")
        print(f"Received new_status: {new_status}")

        # Check if order_id is valid
        if not order_id or not order_id.isdigit():
            return HttpResponse("Invalid order ID", status=400)

        order_id = int(order_id)  # Ensure it is converted to an integer

        # Get the order object
        order = get_object_or_404(Order, pk=order_id)
        order.status = new_status
        order.save()
        return redirect('order_view')






def delete_product(request, product_id):
 
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == "POST":
        product_name = product.name 
        product.delete()
        messages.success(request, f'Product "{product_name}" was deleted successfully.')
        return redirect('product') 

    return render(request, 'product.html', {'products': Product.objects.all()})




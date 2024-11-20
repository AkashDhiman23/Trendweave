import email
from urllib import request
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.core.mail import send_mail # type: ignore
from django.contrib.auth.decorators import login_required
from django.views import View
import stripe
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser ,Wish, Cart ,Order,OrderItem,Payment
from django.contrib.auth import authenticate, login 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .forms import CustomUserForm , LoginForm # Ensure you have a form class for user registration
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.template.loader import render_to_string

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


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









def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')

                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('login')
                else:
                    messages.error(request, "Passwords do not match.")
            return render(request, 'reset_password.html')

        else:
            messages.error(request, "The password reset link is invalid or expired.")
            return redirect('login')

    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('login')















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
    from admin_panel.models import Category, Subcategory, Product
     # Filter the wishlist items for the currently authenticated user
    data = Cart.objects.select_related('product').filter(customuser=request.user)  

    g_total = 0
    for d in data:
        g_total += d.sub_total()  # Assuming this method calculates the subtotal for each item

    # Render the wishlist template with the wishlist data and grand total
    return render(request, 'cart.html', {'data': data, 'g_total': g_total})
  

def delete_cart(request,cart_item_id ):
    c = Cart.objects.get(cart_item_id =cart_item_id )
    c.delete()
    messages.warning(request,'Product is deleted from cart...')
    return redirect('/cart/')


def plus_cart(request,cart_item_id ):
    c = Cart.objects.get(cart_item_id =cart_item_id )
    c.quantity += 1
    c.save()
    messages.success(request,'Quantity is Plus by one...')
    return redirect('/cart/')

def minus_cart(request,cart_item_id ):
    c = Cart.objects.get(cart_item_id =cart_item_id )
    if c.quantity > 1:
        c.quantity -= 1
        c.save()
        messages.info(request,'Quantity is Minus by one...')
    else:
        c.delete()
        messages.info(request,'Quantity is Minus by one...')

    return redirect('/cart/')


    
def search(request):
    from admin_panel.models import Category, Subcategory, Product 
    query = request.GET.get('query')  # This gets the 'query' parameter from the URL
    data = Product.objects.filter(name__icontains=query)  # Change pname to name
    return render(request, 'search.html', {'data': data, 'query': query})


from django.shortcuts import render
from admin_panel.models import Category, Subcategory, Product

def shop(request):
    from admin_panel.models import Category, Subcategory, Product  
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    # Calculate the count of products within each price range
    price_ranges = {
        '0_100': products.filter(price__gte=0, price__lt=100).count(),
        '100_200': products.filter(price__gte=100, price__lt=200).count(),
        '200_300': products.filter(price__gte=200, price__lt=300).count(),
        '300_400': products.filter(price__gte=300, price__lt=400).count(),
        '400_500': products.filter(price__gte=400, price__lt=500).count(),
    }
    
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'products_count': products.count(),
        'price_ranges': price_ranges,
    }
    
    return render(request, 'shop.html', context)


def product(request, product_id):
    from admin_panel.models import Category, Subcategory, Product  # Move import here
    product = get_object_or_404(Product, product_id=product_id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)




def shop_o(request):
    from admin_panel.models import Category, Subcategory, Product  
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    # Calculate the count of products within each price range
    price_ranges = {
        '0_100': products.filter(price__gte=0, price__lt=100).count(),
        '100_200': products.filter(price__gte=100, price__lt=200).count(),
        '200_300': products.filter(price__gte=200, price__lt=300).count(),
        '300_400': products.filter(price__gte=300, price__lt=400).count(),
        '400_500': products.filter(price__gte=400, price__lt=500).count(),
    }
    
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
        'products_count': products.count(),
        'price_ranges': price_ranges,
    }
    
    return render(request, 'shop-o.html', context)




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

    return redirect('shop')



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


def profile(request):
    # Pass the user's data to the template
    context = {
        'customUser': request.user
    }

    return render(request, 'myprofile.html', context)


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





def home(request):
    from admin_panel.models import Category, Subcategory, Product  # Move import here
    products = Product.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'subcategories': subcategories,
    }
    
    return render(request, 'home.html', context)


# Create a logger for debugging
logger = logging.getLogger(__name__)

def checkout(request):
    data = Cart.objects.filter(customuser=request.user)
    g_total = 0
    for d in data:
        g_total += d.sub_total()

    total = g_total + 10  # Fixed shipping fee
    total_in_cents = int(round(total * 100))

    if request.method == 'POST':
        # Get POST data from the form
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        payment = request.POST['payment']

        if payment == '1':  # Cash on Delivery
            order_type = 'Cash On Delivery'
            # Create the order
            order = Order(
                name=name, email=email, phone=phone, address=address,
                city=city, state=state, zip=zip, p_type=order_type,
                customuser=request.user, amount=total
            )
            order.save()

            # Create OrderItems and update product quantities
            for d in data:
                p = Product.objects.get(product_id=d.product.product_id)
                order_item = OrderItem(
                    order=order, product=p, quantity=d.quantity, sub_total=d.sub_total()
                )
                order_item.save()

                # Reduce the product quantity in stock
                p.stock -= d.quantity
                p.save()

                # Delete the cart item after adding it to the order
                d.delete()

            # Send confirmation email
            send_invoice_email(order)

            messages.success(request, 'Order is saved...')
            return redirect('/confirmorder/' + str(order.order_id))

        elif payment == '2':  # Stripe payment
            order_type = 'Stripe'
            order = Order(
                name=name, email=email, phone=phone, address=address,
                city=city, state=state, zip=zip, p_type=order_type,
                customuser=request.user, amount=total
            )
            order.save()

            try:
                stripe_charge = stripe.Charge.create(
                    amount=total_in_cents,
                    currency='usd',
                    description='Fashion Store Checkout',
                    source=request.POST['stripeToken']
                )

                payment = Payment(
                    stripe_charge_id=stripe_charge['id'],
                    customuser=request.user,
                    amount=total_in_cents
                )
                payment.save()

                for d in data:
                    p = Product.objects.get(product_id=d.product.product_id)
                    order_item = OrderItem(
                        order=order, product=p, quantity=d.quantity, sub_total=d.sub_total()
                    )
                    order_item.save()

                    p.stock -= d.quantity
                    p.save()
                    d.delete()

                # Send confirmation email
                send_invoice_email(order)

                messages.success(request, 'Order placed successfully with Stripe payment!')
                return redirect('/confirmorder/' + str(order.order_id))
            except stripe.error.StripeError as e:
                logger.error(f"Stripe error: {str(e)}")
                messages.error(request, 'Error processing payment: ' + str(e))
                return redirect('/checkout/')

    return render(request, 'checkout.html', {'data': data, 'g_total': g_total, 'total': total})




# def send_invoice_email(order):
#     subject = f"Order Confirmation - #{order.order_id}"
#     message = render_to_string('invoice_email.html', {
#         'order': order,
#         'order_items': OrderItem.objects.filter(order=order),
#         'total': order.amount,
#     })
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [order.email],
#         fail_silently=False,
#     )


from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.template.loader import render_to_string


# Function to generate the PDF invoice
def generate_invoice_pdf(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Order #{order.order_id} Invoice")

    # Header
    pdf.drawString(30, 750, f"Order Confirmation - #{order.order_id}")
    pdf.drawString(30, 730, f"Customer: {order.name}")
    pdf.drawString(30, 710, f"Email: {order.email}")
    pdf.drawString(30, 690, f"Order Total: ${order.amount}")
    pdf.drawString(30, 670, "Items:")

    # Add items to the PDF
    y_position = 650
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        pdf.drawString(30, y_position, f"{item.product.name} - Quantity: {item.quantity} ")
        y_position -= 20

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer

# Function to send the invoice email
def send_invoice_email(order):
    # Generate the PDF invoice
    pdf_buffer = generate_invoice_pdf(order)

    # Email subject and body content
    subject = f"Order Confirmation - #{order.order_id}"
    message = render_to_string('invoice_email.html', {
        'order': order,
        'order_items': OrderItem.objects.filter(order=order),
        'total': order.amount,
    })

    # Send the email with the PDF attached
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
        html_message=message,
    )

    # Attach the generated PDF (send_mail does not support attachments, so we need a workaround)
    from django.core.mail import EmailMessage
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )
    email.content_subtype = 'html'
    email.attach(f"Order_{order.order_id}_Invoice.pdf", pdf_buffer.getvalue(), 'application/pdf')
    
    # Send the email with attachment
    email.send(fail_silently=False)

    # Close the PDF buffer
    pdf_buffer.close()




def myorders(request):
    data = Order.objects.filter(customuser=request.user)
    return render(request,'myorder.html',{'data':data})

def confirmorder(request, order_id):
    order_data = Order.objects.get(order_id=order_id)
    order_item_data = OrderItem.objects.filter(order=order_data)  # Filter by the order instance

        # Check if the data exists
    print(order_item_data)  # Add this line to inspect the output in the console.

    return render(request, 'confirmorder.html', {'order_data': order_data, 'order_item_data': order_item_data})


def process_payment(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        try:
            payment_token = request.POST.get('stripeToken')  # Get the token from the form

            if not payment_token:
                return JsonResponse({'success': False, 'error': 'Payment method is required'})

            # Calculate total amount (in cents)
            total_in_cents = int(order.amount * 100)

            # Create a PaymentIntent using the token
            intent = stripe.PaymentIntent.create(
                amount=total_in_cents,  # Amount in cents
                currency='nzd',  # Currency in New Zealand Dollars
                payment_method_data={  # Correct way to pass payment_method_data
                    'type': 'card',
                    'card': {
                        'token': payment_token  # Pass the token here
                    }
                },  # Pass the token directly
                confirm=True,  # Automatically confirm the PaymentIntent
                automatic_payment_methods={  
                    'enabled': True,  # Enable automatic payment methods selection
                },
            )

            if intent.status == 'succeeded':
                order.payment_status = 'Paid'
                order.save()
                return redirect('order_confirmation')  # Redirect to an order confirmation page
            else:
                return JsonResponse({'success': False, 'error': 'Payment failed'})

        except stripe.error.StripeError as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

class PaymentView(View):
    def get(self, *args, **kwargs):
        order_id = kwargs.get('oid')
        try:
            order = Order.objects.get(order_id=order_id)
            context = {
                'order': order,
            }
            return render(self.request, "payment.html", context)
        except Order.DoesNotExist:
            messages.error(self.request, "The requested order does not exist.")
            raise Http404("Order not found")

    def post(self, *args, **kwargs):
        order_id = kwargs.get('oid')
        try:
            order = Order.objects.get(customuser=self.request.user, order_id=order_id)
            stripe_token = self.request.POST.get('stripeToken')
            amount_in_cents = order.amount * 100  # Convert to cents
            
            try:
                intent = stripe.PaymentIntent.create(
                    amount=amount_in_cents,
                    currency="nzd",
                    payment_method=stripe_token,
                    confirm=True,
                )

                # Handle successful payment
                if intent.status == 'succeeded':
                    payment = Payment()
                    payment.stripe_charge_id = intent.id
                    payment.user = self.request.user
                    payment.amount = order.amount
                    payment.save()

                    order.payment = payment
                    order.save()

                    messages.success(self.request, "Order was successful")
                    return redirect('/confirmorder/' + str(order.order_id))

                else:
                    messages.error(self.request, "Payment failed.")
                    return redirect("/home/")

            except stripe.error.StripeError as e:
                messages.error(self.request, f"Stripe error: {e.error.message}")
                return redirect("/home/")

            except Exception as e:
                messages.error(self.request, f"An error occurred: {str(e)}")
                return redirect("/home/")

        except Order.DoesNotExist:
            messages.error(self.request, "The requested order does not exist.")
            return redirect("/home/")
        


def order_cancel(request,order_id):
    order_data = Order.objects.get(order_id=order_id)
    order_data.status = 'CANCEL'
    order_data.save()
    return redirect('/myorders/')



from .forms import PasswordResetRequestForm
from django.utils.crypto import get_random_string

otp_store = {}

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                # Generate a random OTP
                otp = get_random_string(length=6, allowed_chars='0123456789')
                
                # Store email and OTP in the session
                request.session['email'] = email
                request.session['otp'] = otp
                
                # Send OTP to email
                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP for resetting your password is: {otp}',
                    'admin@fashionstore.com',  # Replace with your email
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'OTP sent to your email.')
                return redirect('verify_and_reset')
            except CustomUser.DoesNotExist:  # Update to use your custom user model
                messages.error(request, 'No account found with this email.')
        else:
            messages.error(request, 'Invalid email address.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'forgetpassword.html', {'form': form})




from django.contrib.auth import get_user_model

from django.contrib.auth import get_user_model

def verify_and_reset(request):
    if request.method == "POST":
        # Fetch the data from the POST request
        entered_otp = request.POST.get('otp')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Retrieve email and OTP from the session
        email = request.session.get('email')
        stored_otp = request.session.get('otp')

        # Debugging: Print to verify session values
        print(f"Email from session: {email}")
        print(f"OTP from session: {stored_otp}")

        # Check OTP validity
        if entered_otp == stored_otp:  # Verify OTP
            if new_password1 == new_password2:  # Ensure passwords match
                if email:  # Check if email exists in the session
                    try:
                        # Fetch the user from the database using the email
                        user = get_user_model().objects.get(email=email)

                        # Set the new password and save the user object
                        user.set_password(new_password1)
                        user.save()

                        # Clear session data after successful reset
                        del request.session['email']
                        del request.session['otp']

                        # Success message and redirect to login
                        messages.success(request, "Your password has been reset successfully.")
                        return redirect('login')  # Redirect to the login page after password reset

                    except get_user_model().DoesNotExist:
                        # Handle case where the user is not found
                        messages.error(request, "User not found. Please check the email address.")
                        return redirect('password_reset')  # Redirect back to password reset

                else:
                    messages.error(request, "No email found in session.")
            else:
                messages.error(request, "Passwords do not match. Please try again.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'password_reset_verify.html')


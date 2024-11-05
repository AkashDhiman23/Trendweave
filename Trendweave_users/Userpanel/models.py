from django.db import models# type: ignore
import random
from admin_panel.models import Category, Subcategory, Product 
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password




class CustomUser(models.Model):
    customuser_id = models.CharField(max_length=10, unique=True, primary_key=True)  # 4-digit unique ID as primary key
    first_name = models.CharField(max_length=30)  # First name field
    last_name = models.CharField(max_length=30)   # Last name field
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Password field for hashed password

    last_login = models.DateTimeField(null=True, blank=True)
    def save(self, *args, **kwargs):
        # Ensure customuser_id is unique
        if not self.customuser_id or self.customuser_id == '0000':
            while True:
                random_id = str(random.randint(1000, 9999))  # Generate a 4-digit ID
                if not CustomUser.objects.filter(customuser_id=random_id).exists():  # Ensure uniqueness
                    self.customuser_id = random_id
                    break

        # Hash the password if it’s not already hashed
        if not self.password.startswith('pbkdf2_'):  # Only hash if it's not already hashed
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        # Verify a raw password against the stored hashed password
        return check_password(raw_password, self.password)


class Cart(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Cart item {self.cart_item_id}: {self.customuser.customuser_id} - {self.product.name} x{self.quantity}"
    


class Wish(models.Model):
    cid = models.AutoField(primary_key=True)  # Wishlist ID
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishes')  # Product reference
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishes')  # User reference
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product

    def sub_total(self):
        """Calculate the subtotal for this wishlist item."""
        return self.quantity * self.product.price  # Use self.product, not self.product_id

    def __str__(self):
        return f"{self.customuser.username}'s wishlist: {self.product.name} (x{self.quantity})"




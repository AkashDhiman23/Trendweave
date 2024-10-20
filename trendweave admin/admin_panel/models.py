import random
from django.db import models # type: ignore
from django.utils.text import slugify # type: ignore
import random
import string
from pydantic import ValidationError # type: ignore


class AdminRegister(models.Model):
    admin_id = models.PositiveIntegerField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    company_abn = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Generate a random ID if it does not already exist.
        if not self.admin_id:
            self.admin_id = random.randint(1000, 9999)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Admin ID: {self.admin_id})"


def generate_category_id():
    return str(random.randint(100, 999))


def generate_category_id():
    # Generate a random integer between 100 and 999 as a string
    return str(random.randint(100, 999))

class Category(models.Model):
    category_id = models.CharField(
        max_length=3,
        primary_key=True,  # Make category_id the primary key
        unique=True,
        editable=False,
        default=generate_category_id
    )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.ForeignKey(
        'AdminRegister',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Admin who created or last modified this category"
    )

    class Meta:
        ordering = ['name']
        unique_together = (('admin_id', 'category_id'),)  # Composite unique constraint for admin_id and category_id

    def save(self, *args, **kwargs):
        # Automatically generate category_id if not set
        if not self.category_id:
            self.category_id = generate_category_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





def generate_subcategory_id():
    existing_ids = Subcategory.objects.values_list('subcategory_id', flat=True)
    while True:
        new_id = str(random.randint(0, 99)).zfill(2)  # Two-digit subcategory ID
        if new_id not in existing_ids:
            return new_id

class Subcategory(models.Model):
    subcategory_id = models.CharField(
        max_length=2,
        unique=True,
        editable=False,
        default=generate_subcategory_id,
        primary_key=True  # Make subcategory_id the primary key
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the subcategory")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.ForeignKey(
        'AdminRegister',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Admin who created or last modified this subcategory"
    )

    class Meta:
        ordering = ['name']
        unique_together = (('admin_id', 'category', 'subcategory_id'),)  # Composite unique constraint

    def save(self, *args, **kwargs):
        if not self.subcategory_id:
            self.subcategory_id = generate_subcategory_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

def validate_product_id(value):
    if value < 10000 or value > 99999:
        raise ValidationError('Product ID must be a 5-digit integer.')


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # Use AutoField for auto-incrementing ID
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the product")
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products',
        help_text="Category to which the product belongs"
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        on_delete=models.CASCADE,
        related_name='products',
        help_text="Subcategory to which the product belongs"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(help_text="Number of items available in stock")
    image_1 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Primary image of the product")
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Secondary image of the product")
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Tertiary image of the product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_id = models.ForeignKey(
        'AdminRegister',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Admin who created or last modified this product"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Product ID: {self.product_id})"
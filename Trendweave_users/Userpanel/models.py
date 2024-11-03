from django.db import models# type: ignore
import random
from django.conf import settings # type: ignore
from admin_panel.models import Product


class CustomUser(models.Model):
    customuser_id = models.CharField(max_length=4, unique=True, primary_key=True)  # 4-digit unique ID as primary key
    first_name = models.CharField(max_length=30)  # First name field
    last_name = models.CharField(max_length=30)   # Last name field
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.customuser_id or self.customuser_id == '0000':
            # Generate a unique 4-digit ID
            while True:
                random_id = str(random.randint(1000, 9999))  # Generate a 4-digit number
                if not CustomUser.objects.filter(customuser_id=random_id).exists():  # Check uniqueness
                    self.customuser_id = random_id
                    break
        super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
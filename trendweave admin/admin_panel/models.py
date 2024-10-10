import random
from django.db import models # type: ignore

class AdminRegister(models.Model):
    admin_id = models.PositiveIntegerField(unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    company_abn = models.CharField(max_length=11)  
    address = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)  
    password = models.CharField(max_length=128) 

    def save(self, *args, **kwargs):
        if not self.admin_id:
            self.admin_id = random.randint(1000, 9999)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Admin ID: {self.admin_id})"

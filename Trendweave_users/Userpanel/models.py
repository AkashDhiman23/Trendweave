from django.db import models# type: ignore
import random

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)  # Store the OTP  

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        self.save()
# Create your models here.

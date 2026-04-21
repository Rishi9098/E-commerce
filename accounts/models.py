from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)

    def is_buyer(self):
        return self.role == self.BUYER
    
    def is_seller(self):
        return self.role == self.SELLER
    
    def __str__(self):
        return f"{self.username} ({self.role})"
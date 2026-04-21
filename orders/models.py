from django.db import models
from accounts.models import CustomUser
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        {'pading', 'Pending'},
        {'confirmed', 'Confirmed'},
        {'delivered', 'Delivered'},
    ]
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'ORder #{self.id} by {self.buyer.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name= models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10 , decimal_places=2)

    def get_total(self):
        return self.price * self.Quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
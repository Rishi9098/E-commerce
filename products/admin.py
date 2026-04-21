from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'price', 'quantity', 'created_at']
    list_filter = ['seller']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
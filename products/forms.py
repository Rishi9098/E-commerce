from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['name', 'description', 'price', 'quantity', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':4, 'placeholder':'Describe your product'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min':'0.01', 'step':'0.01', 'placeholder': '0.00'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min':'0', 'placeholder':'0'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0 :
            raise forms.ValidationError("Price must be greter than 0.")
        return price
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity
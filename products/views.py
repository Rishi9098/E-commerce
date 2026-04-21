from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from accounts.decorators import seller_requried
from cart.cart import Cart

def product_list(request):
    cart = Cart(request)
    products = Product.objects.filter(quantity__gt=0)
    return render(request, 'products/product_list.html', {'products': products, 'cart': cart})

def product_detail(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product, 'cart': cart})

@seller_requried
def seller_dashboard(request):
    products = request.user.products.all()
    return render(request, 'products/seller_dashboard.html', {'products': products})

@seller_requried
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product= form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/product_forms.html', {'form':form, 'action': 'Add'})

@seller_requried
def product_edit(request, pk):
    product = get_object_or_404(product, pk=pk, seller=request.user)
    if request.method =='POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfuly')
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_forms.html', {'form': form,'action':'Edit','product':product})

@seller_requried
def product_delete(request, pk):
    product = get_object_or_404(product, pk=pk, seller=request.user)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted successfully')
        return redirect('seller_Dashboard')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
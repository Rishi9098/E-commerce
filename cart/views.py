import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .cart import Cart

def _seller_block(request, cart, is_htmx):
    if request.user.is_authenticated and request.user.is_seller():
        if is_htmx:
            response = HttpResponse(
                f'<span id="cart-count" class="badge bg-danger rounded-pill">{len(cart)}</span>'
            )
            response['HX-Trigger'] = 'sellerCartBlock'
            return response
        messages.error(request, "Sellers cannot use the cart, Go to your dashboard.")
        return redirect('seller_dashboard')
    return None

def cart_detail(request):
    if request.user.is_authenticated and request.user.is_seller():
        messages.error(request, "Sellers cannot access the cart.")
        return redirect('seller_dashboard')
    
    cart = Cart(request)
    items =cart.get_items()
    total = cart.get_total_price()
    return render(request, 'cart/cart.html', {'cart_items': items, 'total': total})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    is_htmx = bool(request.headers.get('HX-Request'))

    blocked = _seller_block(request, cart, is_htmx)
    if blocked:
        return blocked
    
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            raise ValueError
    except (ValueError, TypeError):
        if is_htmx:
            response = HttpResponse(
                f'<span id="cart-count" class="badge bg-danger rounded-pill">{len(cart)}</span>'
            )
            response['HX-Trigger'] = 'cartInvalidQty'
            return response
        messages.error(request, "Invalid quantity.")
        return redirect('product_list')
    
    if product.quantity <= 0:
        if is_htmx:
            response = HttpResponse(
                f'<span id="cart-count" class="badge bg-danger rounded-pill">{len(cart)}</span>'
            )
            response['HX-Trigger'] = 'cartError'
            return response
        messages.error(request, f'"{product.name}" is out of stock.')
        return redirect('product_list')
    
    already_in_cart = cart.get_product_quantity(product.id)
    if already_in_cart + quantity > product.quantity:
        if is_htmx:
            response = HttpResponse(
                 f'<span id="cart-count" class="badge bg-danger rounded-pill"{len(cart)}</span>'
            )
            response['HX-Trigger'] = json.dumps({
                'cartExceedStock': {'available': product.quantity, 'name': product.name}
            })
            return response
        messages.warning(request, f'Only {product.quantity} units available for "{product.name}".')

    cart.add(product, quantity)
    cart_count = len(cart)

    if is_htmx:
        response=HttpResponse(
            f'<span id="cart-count" class="badge bg-danger rounded-pill">{len(cart)}</span>'
        )
        response['HX-Trigger'] = 'cartUpdated'
        return response
    
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('product_list')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    is_htmx = bool(request.headers.get('HX-Request'))

    blocked = _seller_block(request, cart, is_htmx)
    if blocked:
        return blocked
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 0:
            raise ValueError
    except (ValueError, TypeError):
        quantity = 1


    product = get_object_or_404(Product, pk=product_id)
    if quantity > product.quantity:
        quantity = product.quantity

    cart.update(product_id, quantity)
    items = cart.get_items()
    total = cart.get_total_price()
    cart_count = len(cart)

    if is_htmx:
        return render(request, 'cart/partials/cart_items.html',{
            'cart_items': items,
            'total': total,
            'cart_count': cart_count,
            'is_htmx': True,
        })
    
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    is_htmx = bool(request.headers.get('HX-Request'))

    blocked = _seller_block(request, cart, is_htmx)
    if blocked:
        return blocked
    
    cart.remove(product_id)
    items = cart.get_items()
    total = cart.get_total_price()
    cart_count = len(cart)

    if is_htmx:
        return render(request, 'cart/partials/cart_items.html',{
            'cart_items': items,
            'total': total,
            'cart_count': cart_count,
            'is_htmx': True,
        })
    
    return redirect('cart_detail')
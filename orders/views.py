from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.decorators import buyer_required
from cart.cart import Cart
from .models import Order, OrderItem

@buyer_required
def place_order(request):
    cart = Cart(request)
    items = cart.get_items()

    if not items:
        messages.error(request, "Your cart is empty. Add some product first.")
        return redirect('cart_detail')
    
    stock_errors = []
    for item in items:
        if item['product'].quantity <= 0:
            stock_errors.append(f'"{item["product"].name}" is now out of stock.')
        elif item['product'].quantity < item['quantity']:
            stock_errors.append(
                f'"{item["product"].name}": Only {item["product"].quantity} left,'
                f' you have {item["quantity"]} in cart.'
            )
    
    if request.method == 'POST':
        post_errors = []
        for item in items:
            item['product'].refresh_from_db()
            if item['product'].quantity < item['quantity']:
                post_errors.append(f'Stock changed for "{item["product"].name}". Please review your cart.')
        
        if post_errors:
            return render(request, 'orders/order_confirm.html',{
                'cart_items': items,
                'total': cart.get_total_price(),
                'order_errors': post_errors,
                'cart': cart,
            })
        
        order = Order.objects.create(
            buyer= request.user,
            total =cart.get_total_price(),
        )

        for item in items:
            product = item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item['quantity'],
                price=item['price'],
            )
            product.quantity -= item['quantity']
            product.save()

        cart.clear()
        request.session['last_order_id'] = order.id
        return redirect('order_history')
    
    total = cart.get_total_price()
    return render(request, 'orders/order_confirm.html',{
        'cart_items': items,
        'total': total,
        'stock_errors': stock_errors,
        'cart': cart,
    })

@buyer_required
def order_history(request):
    orders = request.user.orders.prefetch_related('items').all()
    last_order_id = request.session.pop('last_order_id', None)
    return render(request, 'orders/order_history.html',{
        'orders': orders,
        'last_order_id': last_order_id,
        'cart': Cart(request),
    })

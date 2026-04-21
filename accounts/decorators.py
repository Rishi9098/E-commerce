from django.shortcuts import redirect
from django.contrib import messages

def seller_requried(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('login')
        if not request.user.is_seller():
            messages.error(request, "Access deniend. This page is for seller only.")
            return redirect('product_list')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

def buyer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login as a buyer to place orders.")
            return redirect('login')
        if not request.user.is_buyer():
            messages.error(request, "Access denied. Omly buyer can place orders.")
            return redirect('product_list')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper
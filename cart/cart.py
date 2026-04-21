from .models import Cart as CartModel, CartItem

class Cart:
    def __init__(self, request):
        self.request = request
        self._cart = self._get_or_create_cart()

    def _get_or_create_cart(self):
        if self.request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=self.request.user)
            return cart
        if not self.request.session.session_key:
            self.request.session.create()
        session_key = self.request.session.session_key
        cart, _ = CartModel.objects.get_or_create(session_key=session_key, user=None)
        return cart
    
    def add(self, product, quantity=1, override_quantity=False):
        item, _ = CartItem.objects.get_or_create(
            cart=self._cart,
            product=product,
            defaults={'price': product.price, 'quantity': 0},
        )
        if override_quantity:
            item.quantity = quantity
        else:
            item.quantity += quantity
        if item.quantity > product.quantity:
            item.quantity = product.quantity
        item.save()

    def update(self, product_id, quantity):
        try:
            item = CartItem.objects.get(cart=self._cart, product_id = product_id)
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()
        except CartItem.DoesNotExist:
            pass

    def remove(self, product_id):
        CartItem.objects.filter(cart=self._cart, product_id=product_id).delete()
    
    def save(self):
        pass

    def clear(self):
        self._cart.items.all().delete()

    def __len__(self):
        return sum(item.quantity for item in self._cart.items.all())
    
    def get_total_price(self):
        return sum(item.price * item.quantity for item in self._cart.items.all())
    
    def get_items(self):
        return[
            {
                'product': item.product,
                'quantity': item.quantity,
                'price': item.price,
                'total': item.price * item.quantity,
            }
            for item in self._cart.items.select_related('product').all()
        ]
    
    def get_product_quantity(self, product_id):
        try:
            return CartItem.objects.get(cart=self._cart, product_id= product_id).quantity
        except CartItem.DoesNotExist:
            return 0
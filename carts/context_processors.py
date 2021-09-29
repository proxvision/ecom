from .models import Cart, CartItem
from .views import _get_cart_id

def counter(request):
    """
    Context processor to dynamically display number of items in cart
    """
    cart_counter = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_items = CartItem.objects.filter(
                cart__cart_id=_get_cart_id(request)
            )
            for cart_item in cart_items:
                cart_counter += cart_item.quantity
        except Cart.DoesNotExist:
            cart_counter = 0
        return dict(cart_counter=cart_counter)

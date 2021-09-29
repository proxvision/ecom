from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, product_id):
    try:
        # Get the cart using the car_id present in the session
        cart = Cart.objects.get(
            cart_id=_get_cart_id(request)
        )
    except Cart.DoesNotExist:
        # If cart doesn't exit, create one
        cart = Cart.objects.create(
            cart_id = _get_cart_id(request)
        )
    # Save present session's cart
    cart.save()
    
    # Get the product
    product = Product.objects.get(id=product_id)
    
    # Add the product to the cart
    try:
        # Check if product is already in cart
        cart_item = CartItem.objects.get(
            product=product, 
            cart=cart
        )
        # If so, increment by 1
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If product not already in cart, create a CartItem object, with the ForeignKeys
        # and starting at the quantity 1
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    ## Test if cart_item has been saved
    # return HttpResponse(cart_item.quantity)
    # exit()
    ## Redirect to URLname 'cart' once item has been added
    return redirect('cart')

def decrement_from_cart(request, product_id):
    # Get current cart
    cart = Cart.objects.get(
        cart_id=_get_cart_id(request)
    )
    # Get the product object that it to be removed
    product = get_object_or_404(
        Product, id=product_id
    )
    # Get the cart_item object that is to be removed using the ForeignKeys
    cart_item = CartItem.objects.get(
        product=product, 
        cart=cart
    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_from_cart(request, product_id):
    # Get current cart
    cart = Cart.objects.get(
        cart_id=_get_cart_id(request)
    )
    # Get the product object that it to be removed
    product = get_object_or_404(
        Product, id=product_id
    )
    # Get the cart_item object that is to be removed using the ForeignKeys
    cart_item = CartItem.objects.get(
        product=product, 
        cart=cart
    )
    cart_item.delete()
    return redirect('cart')

def cart(request, total_price=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        # Get the cart using the car_id present in the session
        cart = Cart.objects.get(
            cart_id=_get_cart_id(request),
        )
        # Get QuerySet of the items in the current cart
        cart_items = CartItem.objects.filter(
            cart=cart,
            is_active=True
        )
        # Iterate through QuerySet to tally up
        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        # Calculate the tax and grand total
        tax = (2 * total_price)/100
        grand_total = total_price + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
             
    return render(request, 'cart.html', context)

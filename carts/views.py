from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, product_id):
    # Get the product
    product = Product.objects.get(id=product_id)
    # Initialise empty variation list
    product_variation = []
    # Check for product variations
    if request.method == 'POST':
       for key in request.POST:
           value = request.POST[key]
           try:
               variation = Variation.object.get(
                   product=product,
                   variation_category__iexact=key, 
                   variation_value__iexact=value
                )
               product_variation.append(variation)
           except:
               pass
        
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
    
    
    # Check if specific product already in cart
    is_product_in_cart = CartItem.objects.filter(
        product=product,
        cart=cart
    ).exists()
    # If so, grab the item(s)
    if is_product_in_cart:
        cart_item = CartItem.object.filter(
            product=product,
            cart=cart
        )
        ## Check if current variation (in product_variations list) exists in models (ie. it's already been added to cart) 
        existing_var_list = []
        item_id_list = []
        for item in cart_item:
            existing_variation = item.variations.all() 
            existing_var_list.append(list(existing_variation)) # Cast QuerySet as List
            item_id_list.append(item.id)
        
        if product_variation in existing_var_list:
            ## Increment this item's (of same variation) quantity
            # Grab corresponding index for item.id when the lists were appended
            item_id_index = existing_var_list.index(product_variation)
            # Grab cart item using product and id 
            item = CartItem.objects.get(
                product=product, 
                id=item_id_list[item_id_index]
            )
            item.quantity += 1
            item.save()
            
        else: 
            ## Initialise one CartItem of this product in this cart session
            item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if product_variation is not None:
                item.variations.clear()
                item.variations.add(*product_variation) # unpack as list
            item.save()
    else:
        # If product not already in cart, create a CartItem object, with the ForeignKeys
        # and starting at the quantity 1
        item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if product_variation is not None:
            item.varations.clear()
            item.variations.add(*product_variation) # unpack as list
        item.save()
    ## Redirect to URLname 'cart' once item has been added
    return redirect('cart')

def decrement_from_cart(request, product_id, cart_item_id):
    # Get current cart
    cart = Cart.objects.get(
        cart_id=_get_cart_id(request)
    )
    # Get the product object that it to be removed
    product = get_object_or_404(
        Product, id=product_id
    )
    
    try:
        # Get the cart_item object that is to be removed using the ForeignKeys
        cart_item = CartItem.objects.get(
            product=product, 
            cart=cart,
            id=cart_item_id
        )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
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
        cart=cart, 
        id=cart_item_id
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

from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _get_cart_id
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request, category_slug=None):
    categories = None
    products = None
    # Check if request includes a slug
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    # Context dictionary to rename objects from Django's default
    context = {
        'products': paged_products, 
    }
    return render(request, 'store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, 
            slug=product_slug
        )
        # Check if there is already a product of the same type added to cart
        is_incart = CartItem.objects.filter(
            cart__cart_id=_get_cart_id(request),
            product=single_product,
        ).exists()
        
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'is_incart': is_incart, 
    }
    return render(request, 'product_detail.html', context)

def search(request):
    if 'q' in request.GET:
        # Grab the value behind the GET key name 'q'
        query = request.GET.get('q')
        # If value is not empty
        if query:
            products = Product.objects.order_by('-created_date').filter(
                # Q objects can utilise '|' (OR)
                Q(product_description__icontains=query) | Q(product_name__icontains=query)
            )
        context = {
            'products': products,
        }
        return render(request, 'store.html', context)

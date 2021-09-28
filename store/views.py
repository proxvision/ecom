from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

def store(request, category_slug=None):
    categories = None
    products = None
    # Check if request includes a slug
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    # Context dictionary to rename objects from Django's default
    context = {
        'products': products, 
    }
    return render(request, 'store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, 
            slug=product_slug
        )
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
    return render(request, 'product_detail.html', context)

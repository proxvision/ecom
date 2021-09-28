from django.views.generic import ListView
from store.models import Product

class HomePageView(ListView):
    queryset = Product.objects.filter(is_available=True)
    context_object_name = 'products'
    template_name = 'home.html'

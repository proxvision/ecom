from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse(
            'product_detail', 
            args=[
                str(self.category.slug), 
                str(self.slug)
            ]
        )
    
    def __str__(self):
        return self.product_name


class VariationManager(model.Model):
    """
    This model inherits from Variation and we define methods to filter 'variation_set', not just '.all' (everything in the set)
    """
    def colours(self):
        return super(Variation, self).filter(variation_category='colour', is_active=True)
    
    def sizes(self):
        return super(Variation, self).filter(variation_category='size', is_active=True)



class Variation(models.Model):
    variation_category_choice = (
        ('colour', 'colour'), 
        ('size', 'size'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value

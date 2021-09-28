from .models import Category

def menu_links(request):
    """
    Generates a QuerySet of all the categories under the 'links' key in a dictionary
    """
    links = Category.objects.all()
    return dict(links=links)

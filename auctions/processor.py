from auctions.views import category


from .models import Categories

def categories (request):
    categories = Categories.objects.all()
    context = {
        'categories': categories
    }

    return context
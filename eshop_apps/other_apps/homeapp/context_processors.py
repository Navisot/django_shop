from ..homeapp.models import Genre
from cart.cart import Cart


def genres_processor(request):
    genres = Genre.objects.all()
    return {'genres': genres}


def get_current_cart(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    return {'total_items': myCart['total_items'], 'total_price': myCart['total_price']}
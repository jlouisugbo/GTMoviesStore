from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from moviepage.models import Movie
from .utils import calculate_cart_total

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(imdb_id=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, imdb_id=id)
    cart = request.session.get('cart', {})
    new_quantity = int(request.POST.get('quantity', 1))
    cart[id] = cart.get(id, 0) + new_quantity
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from moviepage.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        print(f"Movie IDs in cart: {movie_ids}")
        movies_in_cart = Movie.objects.filter(imdb_id__in=movie_ids)
        print(f"Movies in cart: {movies_in_cart}")
        cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, imdb_id=id)
    cart = request.session.get('cart', {})
    if id in cart:
        cart[id] += int(request.POST['quantity'])
    if id not in cart:
        cart[id] = int(request.POST['quantity'])
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

def remove(request, id):
    get_object_or_404(Movie, imdb_id=id)
    cart = request.session.get('cart', {})
    if (cart[id] - 1 > 0):
        cart[id] = int(cart[id] - 1)
    if int (cart[id] - 1 == 0):
        del cart[id]
    request.session['cart'] = cart
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())

    if (movie_ids == []):
        return redirect('cart.index')

    movies_in_cart = Movie.objects.filter(imdb_id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.imdb_id)]
        item.save()

    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
    {'template_data': template_data})
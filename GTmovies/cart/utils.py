def calculate_cart_total(cart, movies_in_cart):
    total = 0
    for movie in movies_in_cart:
        quantity = cart.get(str(movie.id), 0)
        total += movie.price * int(quantity)
    return total
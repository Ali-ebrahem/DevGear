from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product
from django.contrib.auth.decorators import login_required



def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'shop/home.html', {
        'products': products,
        'cart_count': cart_count,
        'query': query,
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_count': cart_count,
    })


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    cart_count = sum(cart.values())

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,
    })

    cart_count = sum(cart.values())

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count,
    })


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'shop/register.html', {'form': form})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    if request.method == 'POST':
        # هنا ممكن بعدين نربط ب Payment
        request.session['cart'] = {}  # تفريغ الكارت
        return render(request, 'shop/success.html')

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })
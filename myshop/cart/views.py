from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product


@require_POST
def cart_add(request, product_id):
    """Это представление добавления товаров в корзину или обновления количества существующих товаров"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product,
                 quantity=data['quantity'],
                 override_quantity=data['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """ Представление удаления товаров из корзины."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Представление отображения корзины и ее товаров."""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )
    return render(request, 'cart/detail.html', {'cart': cart})

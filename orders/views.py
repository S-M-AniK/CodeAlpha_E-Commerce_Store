from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product
from decimal import Decimal


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.get_total()
            order.save()
            for pid, item in cart.cart.items():
                product = Product.objects.get(id=int(pid))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['qty'],
                    price=Decimal(item['price']),
                )
            cart.session.pop('cart', None)
            cart.save()
            return redirect('orders:success', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'orders/create.html', {'form': form, 'cart': cart})


def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/success.html', {'order': order})
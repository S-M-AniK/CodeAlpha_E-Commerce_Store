from decimal import Decimal

CART_SESSION_KEY = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(CART_SESSION_KEY, {})

    def add(self, product, quantity=1, override_qty=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'qty': 0, 'price': str(product.price)}
        if override_qty:
            self.cart[pid]['qty'] = quantity
        else:
            self.cart[pid]['qty'] += quantity
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total(self):
        return sum(Decimal(v['price']) * v['qty'] for v in self.cart.values())

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_items(self):
        from products.models import Product
        items = []
        for pid, data in self.cart.items():
            product = Product.objects.get(id=int(pid))
            items.append({
                'product': product,
                'qty': data['qty'],
                'price': Decimal(data['price']),
                'total': Decimal(data['price']) * data['qty'],
            })
        return items
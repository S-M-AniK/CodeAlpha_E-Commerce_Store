from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'products/detail.html', {'product': product})
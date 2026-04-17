from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def index(request):

    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'store/index.html', context)


def product_info(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'store/product-info.html', context)

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.all().filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'store/category-list.html', context)
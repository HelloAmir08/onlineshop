from typing import Optional
from django.shortcuts import render, get_object_or_404, redirect
from onlineshop.forms import OrderForm, CommentForm, ProductForm
from onlineshop.models import Product, Category, Order, Comment
from django.contrib import messages



# Create your views here.


def index(request, category_id: Optional[int] = None):
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context=context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # product = Product.objects.get(id=pk)
    context = {
        'product': product,
        'comments': product.comments.all(),
    }
    return render(request, 'shop/detail.html', context=context)


def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        form = OrderForm(request.GET)
        if form.is_valid():
            full_name = request.GET.get('full_name')
            phone_number = request.GET.get('phone_number')
            quantity = int(request.GET.get('quantity'))
            if product.quantity >= quantity:
                product.quantity -= quantity
                order = Order.objects.create(
                    full_name=full_name,
                    phone_number=phone_number,
                    quantity=quantity,
                    product=product
                )
                order.save()
                product.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Order successfully created.'

                )

            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Order quantity is less than the product quantity.'
                )


    else:
        form = OrderForm()
    context = {
        'form': form,
        'product': product
    }

    return render(request, 'shop/detail.html', context=context)




def comment_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                product=product,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                description=form.cleaned_data['description']
            )
            return redirect('comment_detail', pk=product.pk)
    else:
        form = CommentForm()
    comments = product.comments.all().order_by('-created_at')
    context = {
        'product': product,
        'form': form,
        'comments': comments,
    }
    return render(request, 'shop/detail.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()

    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'shop/admin_panel/CREATE.html', context=context)


def product_edit(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk)
    context = {
        'form': form,
        'product': product,
        'categories': Category.objects.all(),
    }
    return render(request, 'shop/admin_panel/Update.html', context=context)

def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('products')


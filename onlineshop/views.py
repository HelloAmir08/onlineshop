from typing import Optional
from django.shortcuts import render, get_object_or_404

from onlineshop.forms import OrderForm, CommentForm
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

    return render(request, 'shop/detail.html', {'product': product})


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
    if request.method == 'GET':
        form = CommentForm(request.GET)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            comment = Comment.objects.create(
                product=product,
                full_name=full_name,
                email=email,
                description=description
            )
            comment.save()
    else:
        form = CommentForm()
    comment = Comment.objects.all()
    context = {
        'form': form,
        'product': product,
        'comments': comment,
    }
    return render(request, 'shop/detail.html', context)



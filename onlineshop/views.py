from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from onlineshop.models import Product, Category, Order, Comment
from onlineshop.forms import OrderForm, CommentForm, ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        filter_type = self.request.GET.get('filter', '')
        category_id = self.kwargs.get('category_id')
        products = Product.objects.all()

        if category_id:
            products = products.filter(category_id=category_id)

        if filter_type == 'expensive':
            products = products.order_by('-price')[:5]
        elif filter_type == 'cheap':
            products = products.order_by('price')[:5]
        elif filter_type == 'rating':
            products = products.filter(rating__gte=4).order_by('-rating')

        if search_query:
            products = products.filter(name__icontains=search_query)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(product=self.object)
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
        return context


class OrderCreateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = OrderForm(request.POST)  # Используем POST, а не GET

        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            phone_number = form.cleaned_data.get('phone_number')
            quantity = form.cleaned_data.get('quantity')

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
                messages.success(request, 'Order successfully created.')
            else:
                messages.error(request, 'Order quantity exceeds available stock.')
        else:
            print(form.errors)

        return redirect('product_detail', pk=pk)



class CommentCreateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                product=product,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                description=form.cleaned_data['description']
            )
        return redirect('product_detail', pk=pk)



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/admin_panel/CREATE.html'
    success_url = reverse_lazy('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', None)
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/admin_panel/Update.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', None)
        return context


class ProductDeleteView(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['pk'])
        product.delete()
        return redirect(reverse_lazy('products'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


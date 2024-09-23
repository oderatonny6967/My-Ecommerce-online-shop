from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CheckoutForm
from .models import Product, Order, Cart, Review
from django.contrib import messages
from django.db.models import Q

def index(request):
    products = Product.objects.all()
    return render(request, 'Myecommerce/index.html', {'products': products})

def index2(request):
    products = Product.objects.all()
    return render(request, 'Myecommerce/index2.html', {'products': products})
    
def product_search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'Myecommerce/index.html', {'products': products, 'search_query': query})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Registration successful. Welcome, {user.username}!')
            next_url = request.GET.get('next', 'login')
            return redirect(next_url)
    else:
        form = UserCreationForm()
        next_url = request.GET.get('next', 'login')
    return render(request, 'registration/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Login successful. Welcome, {user.username}!')
            next_url = request.POST.get('next', 'index2')  # Default to 'index' if 'next' is not provided
            return redirect(next_url)
        else:
            return render(request, 'Myecommerce/login.html', {'form': form, 'error_message': 'Invalid login details'})
    else:
        form = AuthenticationForm()
        next_url = request.GET.get('next', 'index2')
        return render(request, 'Myecommerce/login.html', {'form': form, 'next': next_url})



@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.total_price = total
            order.save()
            cart_items.delete()
            return redirect('order_history')
    else:
        form = CheckoutForm()
    return render(request, 'Myecommerce/checkout.html', {'cart_items': cart_items, 'total': total, 'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, 'Myecommerce/order_history.html', {'orders': orders})

def logout_view(request):
    auth_logout(request)
    return redirect('index')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    cart.quantity += 1
    cart.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'Myecommerce/cart.html', {'cart_items': cart_items, 'total': total})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'Myecommerce/product_detail.html', {'product': product, 'reviews': reviews})

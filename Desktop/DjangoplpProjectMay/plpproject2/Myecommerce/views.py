from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from .forms import UserRegisterForm, UserLoginForm, CheckoutForm
from .models import Product, Order, Cart, Review
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'myecommerce/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'myecommerce/login.html', {'form': form})

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer  # Assuming each user has one Customer object associated
            order.total_price = total
            order.save()
            cart_items.delete()
            return redirect('order_history')
    else:
        form = CheckoutForm()
    return render(request, 'myecommerce/checkout.html', {'cart_items': cart_items, 'total': total, 'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, 'myecommerce/order_history.html', {'orders': orders})

def logout_view(request):
    auth_logout(request)
    return redirect('index')

def index(request):
    products = Product.objects.all()
    return render(request, 'myecommerce/index.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'myecommerce/product_detail.html', {'product': product, 'reviews': reviews})

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
    return render(request, 'myecommerce/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer  # Assuming each user has one Customer object associated
            order.total_price = sum(item.product.price * item.quantity for item in Cart.objects.filter(user=request.user))
            order.save()
            Cart.objects.filter(user=request.user).delete()
            return redirect('order_history')
    else:
        form = CheckoutForm()
    return render(request, 'myecommerce/checkout.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    return render(request, 'myecommerce/order_history.html', {'orders': orders})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'myecommerce/login.html')

def user_logout(request):
    auth_logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'myecommerce/register.html', {'form': form})

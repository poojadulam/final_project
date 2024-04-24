from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Product, Order, OrderItem, Category, TableReservation
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import TableReservationForm


# def menu_view(request):
#     products = Product.objects.filter(available=True)
#     return render(request, 'cafe/menu.html', {'products': products})
def menu_view(request):
    # Fetch all categories and prefetch related products
    categories = Category.objects.all().prefetch_related('products')
    return render(request, 'cafe/menu.html', {'categories': categories})

@login_required
def place_order(request):
    if request.method == 'POST':
        product_quantities = request.POST.getlist('product-quantity')
        user = request.user

        with transaction.atomic():  # Ensures all or nothing is committed to the database
            order = Order.objects.create(user=user, total_price=0, status='Pending')
            try:
                for pq in product_quantities:
                    product_id, quantity = pq.split(':')
                    if quantity:
                        quantity = int(quantity)
                        if quantity > 0:  # Ensure a valid quantity
                            product = Product.objects.get(id=product_id)
                            subtotal = product.price * quantity
                            OrderItem.objects.create(order=order, product=product, quantity=quantity, subtotal=subtotal)
                            order.total_price += subtotal
                order.save()
            except Exception as e:
                messages.error(request, f"Error creating order: {e}")
                # Handle the error, such as rolling back the transaction, logging, etc.
                raise  # Or handle the exception (e.g., log it and continue)
                
        return redirect('order_confirmation', order_id=order.id)

    products = Product.objects.filter(available=True)
    return render(request, 'cafe/place_order.html', {'products': products})


def order_confirmation(request, order_id):
    # Retrieve the order using the order_id
    order = get_object_or_404(Order, id=order_id)

    # Pass the order to the template
    return render(request, 'cafe/order_confirmation.html', {'order': order})

def home(request):
    return render(request, 'cafe/home.html')

def new_reservation(request):
    if request.method == 'POST':
        form = TableReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations_list')
    else:
        form = TableReservationForm()
    return render(request, 'cafe/new_reservation.html', {'form': form})

def reservations_list(request):
    reservations = TableReservation.objects.all()
    return render(request, 'cafe/reservations_list.html', {'reservations': reservations})
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page at the app root
    path('menu/', views.menu_view, name='menu'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('new-reservation/', views.new_reservation, name='new_reservation'),
    path('reservations-list/', views.reservations_list, name='reservations_list'),
]
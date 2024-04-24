from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)

class TableReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField()
    status = models.CharField(max_length=10)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, help_text="Unit of measure (e.g., kg, liters, packets)")
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cost per unit")

    def __str__(self):
        return f"{self.name} ({self.unit})"

class InventoryItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=9, decimal_places=2, help_text="Current quantity in stock")
    reorder_threshold = models.DecimalField(max_digits=9, decimal_places=2, help_text="Threshold at which to reorder")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ingredient.name}: {self.quantity} {self.ingredient.unit} in stock"


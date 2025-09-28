from django.db import models
from django.contrib.auth.models import User


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Booking(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    no_of_guests = models.PositiveIntegerField()
    booking_date = models.DateTimeField()
    table_number = models.PositiveIntegerField(null=True, blank=True)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['booking_date']
        unique_together = ['booking_date', 'table_number']

    def __str__(self):
        return f"{self.customer_name} - {self.booking_date.strftime('%Y-%m-%d %H:%M')} ({self.no_of_guests} guests)"

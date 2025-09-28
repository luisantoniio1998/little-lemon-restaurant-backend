from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Menu, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'category', 'available', 'featured', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'customer_name', 'customer_email', 'customer_phone',
            'no_of_guests', 'booking_date', 'table_number', 'special_requests',
            'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate_no_of_guests(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of guests must be greater than zero.")
        if value > 20:
            raise serializers.ValidationError("Maximum 20 guests per booking.")
        return value

    def validate_booking_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return value


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'no_of_guests', 'booking_date', 'table_number', 'special_requests'
        ]

    def validate_no_of_guests(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of guests must be greater than zero.")
        if value > 20:
            raise serializers.ValidationError("Maximum 20 guests per booking.")
        return value

    def validate_booking_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return value
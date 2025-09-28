import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'littlelemon.settings')
django.setup()

from restaurant.models import Menu, Booking
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Create sample menu items
menu_items = [
    {
        'name': 'Greek Salad',
        'description': 'Fresh vegetables with feta cheese, olives, and olive oil dressing',
        'price': Decimal('12.99'),
        'category': 'Appetizers',
        'available': True,
        'featured': True
    },
    {
        'name': 'Bruschetta',
        'description': 'Grilled bread with tomatoes, garlic, and basil',
        'price': Decimal('9.99'),
        'category': 'Appetizers',
        'available': True,
        'featured': False
    },
    {
        'name': 'Grilled Salmon',
        'description': 'Fresh Atlantic salmon with herbs and lemon',
        'price': Decimal('24.99'),
        'category': 'Main Course',
        'available': True,
        'featured': True
    },
    {
        'name': 'Chicken Parmigiana',
        'description': 'Breaded chicken breast with marinara sauce and mozzarella',
        'price': Decimal('19.99'),
        'category': 'Main Course',
        'available': True,
        'featured': False
    },
    {
        'name': 'Margherita Pizza',
        'description': 'Classic pizza with tomato sauce, mozzarella, and fresh basil',
        'price': Decimal('16.99'),
        'category': 'Pizza',
        'available': True,
        'featured': True
    },
    {
        'name': 'Tiramisu',
        'description': 'Classic Italian dessert with coffee-soaked ladyfingers',
        'price': Decimal('7.99'),
        'category': 'Desserts',
        'available': True,
        'featured': False
    },
    {
        'name': 'Lemon Tart',
        'description': 'Fresh lemon curd in a buttery pastry shell',
        'price': Decimal('6.99'),
        'category': 'Desserts',
        'available': True,
        'featured': True
    }
]

print("Creating menu items...")
for item_data in menu_items:
    menu_item, created = Menu.objects.get_or_create(
        name=item_data['name'],
        defaults=item_data
    )
    if created:
        print(f"Created: {menu_item.name}")
    else:
        print(f"Already exists: {menu_item.name}")

# Create sample users and bookings
users_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
]

print("\nCreating users...")
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={**user_data, 'password': 'temppass123'}
    )
    if created:
        user.set_password('temppass123')
        user.save()
        print(f"Created user: {user.username}")
    else:
        print(f"User already exists: {user.username}")

# Create sample bookings
bookings_data = [
    {
        'customer_name': 'John Doe',
        'customer_email': 'john@example.com',
        'customer_phone': '555-0101',
        'no_of_guests': 4,
        'booking_date': timezone.now() + timedelta(days=1),
        'table_number': 5,
        'special_requests': 'Window seat please'
    },
    {
        'customer_name': 'Jane Smith',
        'customer_email': 'jane@example.com',
        'customer_phone': '555-0102',
        'no_of_guests': 2,
        'booking_date': timezone.now() + timedelta(days=2),
        'table_number': 3,
        'special_requests': 'Vegetarian options'
    },
    {
        'customer_name': 'Bob Wilson',
        'customer_email': 'bob@example.com',
        'customer_phone': '555-0103',
        'no_of_guests': 6,
        'booking_date': timezone.now() + timedelta(days=3),
        'table_number': 8,
        'special_requests': 'Birthday celebration'
    }
]

print("\nCreating bookings...")
for i, booking_data in enumerate(bookings_data):
    if i < len(users_data):
        user = User.objects.get(username=users_data[i]['username'])
        booking_data['user'] = user

    booking, created = Booking.objects.get_or_create(
        customer_email=booking_data['customer_email'],
        booking_date=booking_data['booking_date'],
        defaults=booking_data
    )
    if created:
        print(f"Created booking: {booking.customer_name}")
    else:
        print(f"Booking already exists: {booking.customer_name}")

print("\nDatabase populated successfully!")
print(f"Menu items: {Menu.objects.count()}")
print(f"Users: {User.objects.count()}")
print(f"Bookings: {Booking.objects.count()}")
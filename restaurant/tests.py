from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from .models import Menu, Booking


class MenuModelTest(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            name="Grilled Salmon",
            description="Fresh Atlantic salmon with herbs",
            price=Decimal('24.99'),
            category="Main Course",
            available=True,
            featured=True
        )

    def test_menu_creation(self):
        self.assertEqual(self.menu_item.name, "Grilled Salmon")
        self.assertEqual(self.menu_item.price, Decimal('24.99'))
        self.assertTrue(self.menu_item.available)
        self.assertTrue(self.menu_item.featured)

    def test_menu_str_method(self):
        expected_str = f"{self.menu_item.name} - ${self.menu_item.price}"
        self.assertEqual(str(self.menu_item), expected_str)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.booking = Booking.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            customer_phone="123-456-7890",
            no_of_guests=4,
            booking_date=timezone.now() + timedelta(days=1),
            table_number=5,
            user=self.user
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.customer_name, "John Doe")
        self.assertEqual(self.booking.no_of_guests, 4)
        self.assertEqual(self.booking.table_number, 5)
        self.assertEqual(self.booking.user, self.user)

    def test_booking_str_method(self):
        expected_str = f"{self.booking.customer_name} - {self.booking.booking_date.strftime('%Y-%m-%d %H:%M')} ({self.booking.no_of_guests} guests)"
        self.assertEqual(str(self.booking), expected_str)


class MenuAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@test.com',
            password='staffpass123',
            is_staff=True
        )
        self.menu_item = Menu.objects.create(
            name="Test Pizza",
            description="Delicious test pizza",
            price=Decimal('15.99'),
            category="Pizza",
            available=True,
            featured=False
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_get_menu_list_unauthenticated(self):
        url = reverse('menu-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_menu_item_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token(self.user))
        url = reverse('menu-list-create')
        data = {
            'name': 'New Pizza',
            'description': 'Another delicious pizza',
            'price': '18.99',
            'category': 'Pizza',
            'available': True,
            'featured': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)

    def test_create_menu_item_unauthenticated(self):
        url = reverse('menu-list-create')
        data = {
            'name': 'New Pizza',
            'description': 'Another delicious pizza',
            'price': '18.99',
            'category': 'Pizza'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_menu_detail(self):
        url = reverse('menu-detail', kwargs={'pk': self.menu_item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Pizza')

    def test_featured_menu_items(self):
        Menu.objects.create(
            name="Featured Pizza",
            description="Featured test pizza",
            price=Decimal('19.99'),
            category="Pizza",
            available=True,
            featured=True
        )
        url = reverse('featured-menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_menu_by_category(self):
        url = reverse('menu-by-category', kwargs={'category': 'Pizza'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BookingAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@test.com',
            password='staffpass123',
            is_staff=True
        )
        self.booking = Booking.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            no_of_guests=4,
            booking_date=timezone.now() + timedelta(days=1),
            user=self.user
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_get_booking_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token(self.user))
        url = reverse('booking-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_booking_list_unauthenticated(self):
        url = reverse('booking-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token(self.user))
        url = reverse('booking-list-create')
        future_date = timezone.now() + timedelta(days=2)
        data = {
            'customer_name': 'Jane Smith',
            'customer_email': 'jane@example.com',
            'customer_phone': '987-654-3210',
            'no_of_guests': 2,
            'booking_date': future_date.isoformat(),
            'table_number': 3,
            'special_requests': 'Window seat please'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

    def test_create_booking_invalid_guests(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token(self.user))
        url = reverse('booking-list-create')
        future_date = timezone.now() + timedelta(days=2)
        data = {
            'customer_name': 'Jane Smith',
            'customer_email': 'jane@example.com',
            'no_of_guests': 0,
            'booking_date': future_date.isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_can_see_all_bookings(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token(self.staff_user))
        url = reverse('booking-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_user_profile_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token(self.user))
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_token_obtain(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

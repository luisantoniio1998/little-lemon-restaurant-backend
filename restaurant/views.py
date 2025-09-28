from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer, BookingCreateSerializer, UserSerializer


class MenuListCreateView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_menu_items(request):
    featured_items = Menu.objects.filter(featured=True, available=True)
    serializer = MenuSerializer(featured_items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_by_category(request, category):
    menu_items = Menu.objects.filter(category__iexact=category, available=True)
    serializer = MenuSerializer(menu_items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """API overview endpoint for frontend developers"""
    api_urls = {
        'Authentication': {
            'Obtain Token': '/api/token/',
            'Refresh Token': '/api/token/refresh/',
        },
        'Menu': {
            'List Menu Items': '/restaurant/menu/',
            'Create Menu Item': '/restaurant/menu/ (POST)',
            'Get Menu Item': '/restaurant/menu/{id}/',
            'Update Menu Item': '/restaurant/menu/{id}/ (PUT/PATCH)',
            'Delete Menu Item': '/restaurant/menu/{id}/ (DELETE)',
            'Featured Items': '/restaurant/menu/featured/',
            'By Category': '/restaurant/menu/category/{category}/',
        },
        'Bookings': {
            'List Bookings': '/restaurant/booking/',
            'Create Booking': '/restaurant/booking/ (POST)',
            'Get Booking': '/restaurant/booking/{id}/',
            'Update Booking': '/restaurant/booking/{id}/ (PUT/PATCH)',
            'Cancel Booking': '/restaurant/booking/{id}/ (DELETE)',
        },
        'User': {
            'User Profile': '/restaurant/profile/',
        },
        'Admin': {
            'Django Admin': '/admin/',
            'API Browser': '/api-auth/',
        }
    }
    return Response(api_urls)


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_categories(request):
    """Get all unique menu categories"""
    categories = Menu.objects.values_list('category', flat=True).distinct().order_by('category')
    return Response(sorted(set(categories)))

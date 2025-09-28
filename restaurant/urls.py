from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('menu/', views.MenuListCreateView.as_view(), name='menu-list-create'),
    path('menu/<int:pk>/', views.MenuDetailView.as_view(), name='menu-detail'),
    path('menu/featured/', views.featured_menu_items, name='featured-menu'),
    path('menu/categories/', views.menu_categories, name='menu-categories'),
    path('menu/category/<str:category>/', views.menu_by_category, name='menu-by-category'),
    path('booking/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('profile/', views.user_profile, name='user-profile'),
]
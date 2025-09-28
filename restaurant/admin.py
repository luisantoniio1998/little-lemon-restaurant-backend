from django.contrib import admin
from .models import Menu, Booking


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'featured', 'created_at']
    list_filter = ['category', 'available', 'featured', 'created_at']
    search_fields = ['name', 'description', 'category']
    list_editable = ['available', 'featured', 'price']
    ordering = ['category', 'name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Availability', {
            'fields': ('available', 'featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_email', 'no_of_guests', 'booking_date', 'table_number', 'user', 'created_at']
    list_filter = ['booking_date', 'no_of_guests', 'table_number', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    date_hierarchy = 'booking_date'
    ordering = ['booking_date']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Booking Details', {
            'fields': ('no_of_guests', 'booking_date', 'table_number', 'special_requests')
        }),
        ('User Association', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

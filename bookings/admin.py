from django.contrib import admin
from .models import Event, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'capacity', 'price_per_person', 'available', 'created']
    list_filter = ['available', 'event_type', 'created']
    list_editable = ['available']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'event', 'event_date', 'event_time', 'number_of_guests', 'total_price', 'payment_status', 'status', 'created']
    list_filter = ['status', 'payment_status', 'event_date', 'created']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'payment_reference']
    date_hierarchy = 'event_date'
    readonly_fields = ['payment_reference', 'paystack_reference', 'payment_date', 'created', 'updated']

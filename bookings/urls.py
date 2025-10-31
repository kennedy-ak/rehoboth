from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'),
]

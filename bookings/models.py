from django.db import models
from django.urls import reverse

class Event(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday Party'),
        ('corporate', 'Corporate Event'),
        ('anniversary', 'Anniversary'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    image = models.ImageField(upload_to='events/%Y/%m/%d', blank=True)
    capacity = models.PositiveIntegerField(help_text='Maximum number of guests')
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookings:event_detail', args=[self.id])


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    event = models.ForeignKey(Event, related_name='bookings', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_date = models.DateField()
    event_time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment fields
    payment_reference = models.CharField(max_length=200, unique=True, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    paystack_reference = models.CharField(max_length=200, null=True, blank=True)

    # SMS notification status
    confirmation_sms_sent = models.BooleanField(default=False)
    payment_sms_sent = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.event.name} on {self.event_date}'

    def get_total_price(self):
        return self.event.price_per_person * self.number_of_guests

    def generate_payment_reference(self):
        """Generate a unique payment reference"""
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8].upper()
        self.payment_reference = f'RHB-{timestamp}-{unique_id}'
        return self.payment_reference

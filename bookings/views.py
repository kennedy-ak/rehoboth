from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
from .models import Event, Booking
from .forms import BookingForm
from .paystack import PaystackAPI
from .sms import send_booking_confirmation_sms, send_payment_confirmation_sms

def event_list(request):
    events = Event.objects.filter(available=True)
    return render(request, 'bookings/event/list.html', {
        'events': events
    })

def event_detail(request, id):
    event = get_object_or_404(Event, id=id, available=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            # Calculate total price
            booking.total_price = event.price_per_person * booking.number_of_guests

            # Check if number of guests doesn't exceed capacity
            if booking.number_of_guests > event.capacity:
                messages.error(request, f'Sorry, this event has a maximum capacity of {event.capacity} guests.')
            else:
                # Generate payment reference
                booking.generate_payment_reference()
                booking.save()

                # Initialize Paystack payment
                paystack = PaystackAPI()
                callback_url = request.build_absolute_uri(
                    reverse('bookings:payment_callback')
                )

                metadata = {
                    'booking_id': booking.id,
                    'event_name': event.name,
                    'customer_name': f'{booking.first_name} {booking.last_name}',
                    'event_date': str(booking.event_date),
                    'number_of_guests': booking.number_of_guests,
                }

                response = paystack.initialize_transaction(
                    email=booking.email,
                    amount=booking.total_price,
                    reference=booking.payment_reference,
                    callback_url=callback_url,
                    metadata=metadata
                )

                if response.get('status'):
                    # Redirect to Paystack payment page
                    authorization_url = response['data']['authorization_url']
                    return redirect(authorization_url)
                else:
                    messages.error(request, 'Payment initialization failed. Please try again.')
    else:
        form = BookingForm()

    return render(request, 'bookings/event/detail.html', {
        'event': event,
        'form': form,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    })

@csrf_exempt
def payment_callback(request):
    """Handle Paystack payment callback"""
    reference = request.GET.get('reference')

    if not reference:
        messages.error(request, 'Invalid payment reference.')
        return redirect('bookings:event_list')

    # Verify the transaction
    paystack = PaystackAPI()
    response = paystack.verify_transaction(reference)

    if response.get('status') and response['data']['status'] == 'success':
        # Get booking by payment reference
        try:
            booking = Booking.objects.get(payment_reference=reference)

            # Update booking payment status
            booking.payment_status = True
            booking.status = 'paid'
            booking.payment_date = datetime.now()
            booking.paystack_reference = response['data']['reference']
            booking.save()

            # Send payment confirmation SMS
            try:
                send_payment_confirmation_sms(booking)
                booking.payment_sms_sent = True
                booking.save()
            except Exception as e:
                print(f"SMS sending failed: {e}")

            messages.success(request, 'Payment successful! You will receive a confirmation SMS shortly.')
            return redirect('bookings:booking_success', booking_id=booking.id)

        except Booking.DoesNotExist:
            messages.error(request, 'Booking not found.')
            return redirect('bookings:event_list')
    else:
        messages.error(request, 'Payment verification failed. Please contact us if you were charged.')
        return redirect('bookings:event_list')

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking/success.html', {
        'booking': booking
    })

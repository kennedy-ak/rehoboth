import requests
from django.conf import settings

class MNotifyAPI:
    """mNotify SMS integration utility"""

    BASE_URL = "https://api.mnotify.com/api"

    def __init__(self):
        self.api_key = settings.MNOTIFY_API_KEY

    def send_sms(self, recipient, message, sender_id=None):
        """
        Send SMS via mNotify

        Args:
            recipient: Phone number (e.g., '233241234567')
            message: SMS message content
            sender_id: Optional sender ID (default from settings)

        Returns:
            dict: API response
        """
        url = f"{self.BASE_URL}/sms/quick"

        if sender_id is None:
            sender_id = getattr(settings, 'MNOTIFY_SENDER_ID', 'Rehoboth')

        # Ensure phone number is in correct format
        recipient = self._format_phone_number(recipient)

        data = {
            'key': self.api_key,
            'to': recipient,
            'msg': message,
            'sender_id': sender_id,
        }

        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def send_bulk_sms(self, recipients, message, sender_id=None):
        """
        Send SMS to multiple recipients

        Args:
            recipients: List of phone numbers
            message: SMS message content
            sender_id: Optional sender ID

        Returns:
            dict: API response
        """
        url = f"{self.BASE_URL}/sms/quick"

        if sender_id is None:
            sender_id = getattr(settings, 'MNOTIFY_SENDER_ID', 'Rehoboth')

        # Format all phone numbers
        recipients = [self._format_phone_number(num) for num in recipients]

        data = {
            'key': self.api_key,
            'to': ','.join(recipients),
            'msg': message,
            'sender_id': sender_id,
        }

        try:
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _format_phone_number(self, phone):
        """
        Format phone number to international format without + sign

        Args:
            phone: Phone number in various formats

        Returns:
            str: Formatted phone number (e.g., '233241234567')
        """
        # Remove all non-digit characters
        phone = ''.join(filter(str.isdigit, phone))

        # If starts with 0, replace with country code 233
        if phone.startswith('0'):
            phone = '233' + phone[1:]

        # If doesn't start with country code, add 233
        if not phone.startswith('233'):
            phone = '233' + phone

        return phone

    def check_balance(self):
        """
        Check mNotify account balance

        Returns:
            dict: Balance information
        """
        url = f"{self.BASE_URL}/balance"

        data = {
            'key': self.api_key,
        }

        try:
            response = requests.get(url, params=data)
            return response.json()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


def send_booking_confirmation_sms(booking):
    """
    Send booking confirmation SMS to customer

    Args:
        booking: Booking instance

    Returns:
        dict: SMS API response
    """
    sms = MNotifyAPI()

    message = (
        f"Dear {booking.first_name}, your booking for {booking.event.name} "
        f"on {booking.event_date.strftime('%d/%m/%Y')} at {booking.event_time.strftime('%I:%M %p')} "
        f"has been confirmed! Booking Ref: #{booking.id}. "
        f"Total: GH₵{booking.total_price}. We look forward to serving you! - Rehoboth Space"
    )

    return sms.send_sms(booking.phone, message)


def send_payment_confirmation_sms(booking):
    """
    Send payment confirmation SMS to customer

    Args:
        booking: Booking instance

    Returns:
        dict: SMS API response
    """
    sms = MNotifyAPI()

    message = (
        f"Payment confirmed! Dear {booking.first_name}, we have received your payment of "
        f"GH₵{booking.total_price} for {booking.event.name}. "
        f"Booking Ref: #{booking.id}. Thank you! - Rehoboth Space"
    )

    return sms.send_sms(booking.phone, message)

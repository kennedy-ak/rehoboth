import requests
from django.conf import settings

class PaystackAPI:
    """Paystack payment integration utility"""

    BASE_URL = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.public_key = settings.PAYSTACK_PUBLIC_KEY
        self.headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }

    def initialize_transaction(self, email, amount, reference, callback_url, metadata=None):
        """
        Initialize a Paystack transaction

        Args:
            email: Customer's email
            amount: Amount in kobo (multiply cedis by 100)
            reference: Unique transaction reference
            callback_url: URL to redirect after payment
            metadata: Optional dictionary with extra data

        Returns:
            dict: API response
        """
        url = f"{self.BASE_URL}/transaction/initialize"

        data = {
            'email': email,
            'amount': int(amount * 100),  # Convert to kobo (pesewas)
            'reference': reference,
            'callback_url': callback_url,
        }

        if metadata:
            data['metadata'] = metadata

        try:
            response = requests.post(url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            return {'status': False, 'message': str(e)}

    def verify_transaction(self, reference):
        """
        Verify a Paystack transaction

        Args:
            reference: Transaction reference

        Returns:
            dict: API response with transaction details
        """
        url = f"{self.BASE_URL}/transaction/verify/{reference}"

        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            return {'status': False, 'message': str(e)}

    def get_transaction(self, transaction_id):
        """
        Get transaction details

        Args:
            transaction_id: Paystack transaction ID

        Returns:
            dict: Transaction details
        """
        url = f"{self.BASE_URL}/transaction/{transaction_id}"

        try:
            response = requests.get(url, headers=self.headers)
            return response.json()
        except Exception as e:
            return {'status': False, 'message': str(e)}

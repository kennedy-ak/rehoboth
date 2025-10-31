from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': '',  # Will be set via JavaScript
        })
    )
    event_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'event_date', 'event_time', 'number_of_guests', 'special_requests']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Number of Guests'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any special requests or dietary requirements?'}),
        }

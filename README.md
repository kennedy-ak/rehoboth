# Rehoboth

A comprehensive Django-based e-commerce and event booking platform that combines online shopping with event management capabilities.

## Features

### E-Commerce Functionality
- **Product Catalog**: Browse products by categories with pagination
- **Shopping Cart**: Session-based cart management
- **Order Management**: Complete order processing system
- **Product Images**: Image upload and management with Pillow

### Event Booking System
- **Event Management**: Create and manage various event types (weddings, birthdays, corporate events, anniversaries)
- **Booking System**: Online booking with capacity management
- **Payment Integration**: Paystack payment gateway integration
- **SMS Notifications**: Automated SMS confirmations via mNotify API

### Technical Features
- **Django Framework**: Built with Django 5.2.6
- **Database**: SQLite3 for development
- **Media Management**: Static and media file handling
- **Admin Interface**: Django admin for content management
- **Responsive Templates**: HTML templates with base layout

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rehoboth
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Configure API keys**:
   - Update `PAYSTACK_PUBLIC_KEY` and `PAYSTACK_SECRET_KEY` in `rehoboth/settings.py`
   - Update `MNOTIFY_API_KEY` in `rehoboth/settings.py`

## Usage

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

3. **Key URLs**:
   - `/`: Product catalog
   - `/cart/`: Shopping cart
   - `/orders/`: Order management
   - `/bookings/`: Event booking system
   - `/admin/`: Django admin interface

## Project Structure

```
rehoboth/
├── bookings/          # Event booking app
├── cart/             # Shopping cart app
├── orders/           # Order management app
├── shop/             # Product catalog app
├── rehoboth/         # Main project settings
├── templates/        # HTML templates
├── static/           # Static files
├── media/            # User-uploaded media
├── manage.py         # Django management script
└── requirements.txt  # Python dependencies
```

## Apps Overview

### Shop App
- Product and category models
- Product listing and detail views
- Category-based filtering

### Cart App
- Session-based cart functionality
- Add/remove products
- Cart context processor

### Orders App
- Order creation and management
- Order items tracking
- Payment status handling

### Bookings App
- Event models with types and capacity
- Booking system with payment integration
- SMS notifications for confirmations
- Paystack payment processing

## Configuration

### Paystack Integration
Replace the placeholder keys in `settings.py`:
```python
PAYSTACK_PUBLIC_KEY = 'your_actual_public_key'
PAYSTACK_SECRET_KEY = 'your_actual_secret_key'
```

### SMS Notifications
Configure mNotify API:
```python
MNOTIFY_API_KEY = 'your_mnotify_api_key'
MNOTIFY_SENDER_ID = 'YourSenderID'
```

## Development

- **Database**: SQLite3 (configured in settings.py)
- **Debug Mode**: Enabled by default (set DEBUG=False for production)
- **Static Files**: Served via Django's staticfiles app
- **Media Files**: Served in debug mode via URL patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if any)
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
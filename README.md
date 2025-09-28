# Little Lemon Restaurant API

A comprehensive Django REST Framework backend system for Little Lemon Restaurant, supporting menu management, table bookings, and customer services.

## 🍋 Project Overview

Little Lemon Restaurant API provides a complete backend solution for restaurant operations including:
- **Menu Management**: CRUD operations for restaurant menu items
- **Booking System**: Customer table reservations with user authentication
- **User Management**: JWT-based authentication and user profiles
- **Admin Interface**: Django admin for restaurant staff management

## 🧰 Tech Stack

- **Backend**: Django 5.2.6
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Testing**: Django Test Framework
- **Documentation**: Built-in DRF Browsable API

## 📋 Features

### Menu Management
- ✅ List all menu items (public access)
- ✅ Create, update, delete menu items (authenticated users)
- ✅ Filter by category and featured items
- ✅ Price validation and availability status

### Booking System
- ✅ Create table reservations (authenticated users)
- ✅ View personal bookings (users see only their bookings)
- ✅ Staff can view all bookings
- ✅ Date/time validation and guest count limits
- ✅ Special requests and table assignments

### Authentication & Authorization
- ✅ JWT token-based authentication
- ✅ User registration and profile management
- ✅ Role-based permissions (staff vs customers)
- ✅ Secure API endpoints

### Admin Interface
- ✅ Django admin with custom configurations
- ✅ Menu item management with filtering
- ✅ Booking management with date hierarchy
- ✅ User permission controls

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone and Setup Environment**
```bash
git clone <repository-url>
cd little-lemon-restaurant
python3 -m venv littlelemon_env
source littlelemon_env/bin/activate  # On Windows: littlelemon_env\\Scripts\\activate
```

2. **Install Dependencies**
```bash
pip install django djangorestframework djangorestframework-simplejwt
```

3. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create Superuser**
```bash
python manage.py createsuperuser
```

5. **Populate Sample Data (Optional)**
```bash
python populate_db.py
```

6. **Run Development Server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📡 API Endpoints

### Authentication
| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/token/` | POST | Obtain JWT tokens | None |
| `/api/token/refresh/` | POST | Refresh access token | None |

### Menu Management
| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/restaurant/menu/` | GET | List all menu items | None |
| `/restaurant/menu/` | POST | Create menu item | Required |
| `/restaurant/menu/{id}/` | GET | Get specific menu item | None |
| `/restaurant/menu/{id}/` | PUT/PATCH | Update menu item | Required |
| `/restaurant/menu/{id}/` | DELETE | Delete menu item | Required |
| `/restaurant/menu/featured/` | GET | Get featured items | None |
| `/restaurant/menu/category/{category}/` | GET | Get items by category | None |

### Booking Management
| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/restaurant/booking/` | GET | List user's bookings | Required |
| `/restaurant/booking/` | POST | Create new booking | Required |
| `/restaurant/booking/{id}/` | GET | Get specific booking | Required |
| `/restaurant/booking/{id}/` | PUT/PATCH | Update booking | Required |
| `/restaurant/booking/{id}/` | DELETE | Cancel booking | Required |

### User Profile
| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/restaurant/profile/` | GET | Get user profile | Required |

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. **Obtain Token**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \\
  -H "Content-Type: application/json" \\
  -d '{"username": "your_username", "password": "your_password"}'
```

2. **Use Token in Requests**
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \\
  http://127.0.0.1:8000/restaurant/booking/
```

## 📊 Sample API Usage

### Create a Menu Item
```bash
curl -X POST http://127.0.0.1:8000/restaurant/menu/ \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Pasta Carbonara",
    "description": "Classic Italian pasta with eggs, cheese, and pancetta",
    "price": "18.99",
    "category": "Main Course",
    "available": true,
    "featured": false
  }'
```

### Create a Booking
```bash
curl -X POST http://127.0.0.1:8000/restaurant/booking/ \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "customer_name": "John Smith",
    "customer_email": "john@example.com",
    "customer_phone": "555-0123",
    "no_of_guests": 4,
    "booking_date": "2024-12-25T19:00:00Z",
    "table_number": 5,
    "special_requests": "Window seat preferred"
  }'
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python manage.py test
```

The test suite includes:
- Model validation tests
- API endpoint tests
- Authentication tests
- Permission tests
- Data validation tests

## 🛠 Development

### Project Structure
```
little-lemon-restaurant/
├── littlelemon/           # Main project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI configuration
├── restaurant/           # Main application
│   ├── models.py        # Menu and Booking models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin configuration
│   └── tests.py         # Test suite
├── manage.py            # Django management
├── populate_db.py       # Sample data script
└── README.md           # This file
```

### Key Models

**Menu Model**
- `name`: Unique menu item name
- `description`: Item description
- `price`: Decimal price field
- `category`: Item category
- `available`: Availability status
- `featured`: Featured item flag

**Booking Model**
- `customer_name`: Customer name
- `customer_email`: Contact email
- `no_of_guests`: Party size (1-20)
- `booking_date`: Reservation datetime
- `table_number`: Assigned table
- `user`: Associated user account

## 🔧 Configuration

### Environment Variables (Production)
```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=yourdomain.com
```

### Django Settings Highlights
- JWT token lifetime: 60 minutes
- Pagination: 20 items per page
- Timezone: UTC
- Authentication: JWT + Session

## 🚀 Deployment

### Heroku Deployment
1. Install dependencies: `pip install gunicorn psycopg2-binary`
2. Create `Procfile`: `web: gunicorn littlelemon.wsgi`
3. Configure environment variables
4. Deploy: `git push heroku main`

### Other Platforms
- **Render**: Works with included configuration
- **Railway**: Compatible with Django apps
- **DigitalOcean**: App Platform ready

## 📝 API Documentation

Interactive API documentation is available at:
- **Browsable API**: `http://127.0.0.1:8000/api-auth/`
- **Admin Interface**: `http://127.0.0.1:8000/admin/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues:
1. Check the browsable API documentation
2. Review the test suite for examples
3. Open an issue on GitHub

---

**Little Lemon Restaurant** - Bringing Italian flavors to your table! 🍋🇮🇹
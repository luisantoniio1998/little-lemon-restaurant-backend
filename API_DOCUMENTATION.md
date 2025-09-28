# Little Lemon Restaurant API Documentation

## Base URL
```
http://127.0.0.1:8000/
```

## Authentication
All protected endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Response Format
All responses are in JSON format with the following structure:

### Success Response
```json
{
    "id": 1,
    "field1": "value1",
    "field2": "value2"
}
```

### Error Response
```json
{
    "detail": "Error message",
    "field_errors": {
        "field_name": ["Field specific error"]
    }
}
```

## Endpoints

### Authentication Endpoints

#### Obtain JWT Token
**POST** `/api/token/`

Request body:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token
**POST** `/api/token/refresh/`

Request body:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Menu Endpoints

#### List Menu Items
**GET** `/restaurant/menu/`

**Authentication:** Not required

Query parameters:
- `page`: Page number for pagination
- `page_size`: Number of items per page (max 20)

Response:
```json
{
    "count": 7,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Greek Salad",
            "description": "Fresh vegetables with feta cheese, olives, and olive oil dressing",
            "price": "12.99",
            "category": "Appetizers",
            "available": true,
            "featured": true,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Create Menu Item
**POST** `/restaurant/menu/`

**Authentication:** Required

Request body:
```json
{
    "name": "Pasta Carbonara",
    "description": "Classic Italian pasta with eggs, cheese, and pancetta",
    "price": "18.99",
    "category": "Main Course",
    "available": true,
    "featured": false
}
```

Response: Returns the created menu item with HTTP 201 status.

#### Get Menu Item
**GET** `/restaurant/menu/{id}/`

**Authentication:** Not required

Response:
```json
{
    "id": 1,
    "name": "Greek Salad",
    "description": "Fresh vegetables with feta cheese, olives, and olive oil dressing",
    "price": "12.99",
    "category": "Appetizers",
    "available": true,
    "featured": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Update Menu Item
**PUT/PATCH** `/restaurant/menu/{id}/`

**Authentication:** Required

Request body (PUT - all fields required, PATCH - partial update):
```json
{
    "name": "Updated Greek Salad",
    "description": "Updated description",
    "price": "13.99",
    "category": "Appetizers",
    "available": true,
    "featured": false
}
```

#### Delete Menu Item
**DELETE** `/restaurant/menu/{id}/`

**Authentication:** Required

Response: HTTP 204 No Content

#### Get Featured Menu Items
**GET** `/restaurant/menu/featured/`

**Authentication:** Not required

Response:
```json
[
    {
        "id": 1,
        "name": "Greek Salad",
        "description": "Fresh vegetables with feta cheese, olives, and olive oil dressing",
        "price": "12.99",
        "category": "Appetizers",
        "available": true,
        "featured": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
]
```

#### Get Menu Items by Category
**GET** `/restaurant/menu/category/{category}/`

**Authentication:** Not required

Example: `/restaurant/menu/category/Pizza/`

Response: Array of menu items in the specified category.

### Booking Endpoints

#### List Bookings
**GET** `/restaurant/booking/`

**Authentication:** Required

Note: Regular users see only their bookings, staff users see all bookings.

Response:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "customer_phone": "555-0101",
            "no_of_guests": 4,
            "booking_date": "2024-01-20T19:00:00Z",
            "table_number": 5,
            "special_requests": "Window seat please",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "user": {
                "id": 2,
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        }
    ]
}
```

#### Create Booking
**POST** `/restaurant/booking/`

**Authentication:** Required

Request body:
```json
{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "customer_phone": "555-0102",
    "no_of_guests": 2,
    "booking_date": "2024-01-25T19:30:00Z",
    "table_number": 3,
    "special_requests": "Vegetarian options"
}
```

Validation rules:
- `no_of_guests`: Must be between 1 and 20
- `booking_date`: Must be in the future
- `customer_email`: Must be valid email format

#### Get Booking
**GET** `/restaurant/booking/{id}/`

**Authentication:** Required

Note: Users can only access their own bookings unless they are staff.

#### Update Booking
**PUT/PATCH** `/restaurant/booking/{id}/`

**Authentication:** Required

Request body (similar to create booking):
```json
{
    "customer_name": "Jane Smith Updated",
    "customer_email": "jane@example.com",
    "customer_phone": "555-0102",
    "no_of_guests": 3,
    "booking_date": "2024-01-25T20:00:00Z",
    "table_number": 4,
    "special_requests": "Updated special requests"
}
```

#### Cancel Booking
**DELETE** `/restaurant/booking/{id}/`

**Authentication:** Required

Response: HTTP 204 No Content

### User Profile Endpoint

#### Get User Profile
**GET** `/restaurant/profile/`

**Authentication:** Required

Response:
```json
{
    "id": 2,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

## Error Codes

| HTTP Status | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Resource deleted successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

## Common Error Responses

### Authentication Required
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Invalid Token
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

### Validation Error
```json
{
    "no_of_guests": [
        "Number of guests must be greater than zero."
    ],
    "booking_date": [
        "Booking date cannot be in the past."
    ]
}
```

### Permission Denied
```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Rate Limiting
Currently, there are no rate limits implemented, but they can be added using Django REST Framework throttling.

## Pagination
List endpoints use page-based pagination:
- Default page size: 20 items
- Maximum page size: 20 items
- Use `?page=2` to get the next page
- Response includes `count`, `next`, and `previous` fields

## Data Formats
- **Dates**: ISO 8601 format (`2024-01-25T19:30:00Z`)
- **Decimals**: String format for prices (`"18.99"`)
- **Booleans**: `true` or `false`

## Testing the API

You can test the API using tools like:
- **curl** (command line)
- **Postman** (GUI client)
- **httpie** (command line)
- **DRF Browsable API** (web interface at `/api-auth/`)

### Example curl commands:

```bash
# Get menu items
curl -X GET http://127.0.0.1:8000/restaurant/menu/

# Login to get token
curl -X POST http://127.0.0.1:8000/api/token/ \\
  -H "Content-Type: application/json" \\
  -d '{"username": "admin", "password": "admin123"}'

# Create booking with token
curl -X POST http://127.0.0.1:8000/restaurant/booking/ \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"customer_name": "Test User", "customer_email": "test@example.com", "no_of_guests": 2, "booking_date": "2024-12-25T19:00:00Z"}'
```
# Little Lemon Frontend Integration Guide

This guide will help you connect your friend's Little Lemon frontend with this Django REST API backend to create a complete full-stack application.

## 🔗 Quick Setup

### 1. Backend Preparation (Already Done!)
✅ CORS configured for frontend communication
✅ JWT authentication implemented
✅ All necessary API endpoints created
✅ Sample data populated

### 2. Frontend Integration Steps

#### Step 1: Clone Frontend Repository
```bash
# Navigate to your projects directory
cd /path/to/your/projects

# Clone your friend's frontend repository
git clone <frontend-repository-url>
cd little-lemon-frontend

# Install dependencies (React/Vue/Angular)
npm install
# or
yarn install
```

#### Step 2: Configure API Base URL
Update the frontend's API configuration to point to your backend:

**For React/JavaScript:**
```javascript
// config/api.js or similar
const API_BASE_URL = 'http://127.0.0.1:8000';

export default API_BASE_URL;
```

**For environment variables:**
```bash
# .env file
REACT_APP_API_URL=http://127.0.0.1:8000
# or
VITE_API_URL=http://127.0.0.1:8000
```

#### Step 3: Update Authentication
Modify the frontend authentication to use JWT tokens:

```javascript
// Example authentication service
class AuthService {
  async login(username, password) {
    const response = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (data.access) {
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
    }
    return data;
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  isAuthenticated() {
    return !!this.getToken();
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}
```

#### Step 4: API Integration Examples

**Fetch Menu Items:**
```javascript
async function fetchMenuItems() {
  const response = await fetch('http://127.0.0.1:8000/restaurant/menu/');
  const data = await response.json();
  return data.results; // DRF pagination format
}
```

**Create Booking (Authenticated):**
```javascript
async function createBooking(bookingData) {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://127.0.0.1:8000/restaurant/booking/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(bookingData),
  });
  return response.json();
}
```

**Fetch User Profile:**
```javascript
async function fetchUserProfile() {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://127.0.0.1:8000/restaurant/profile/', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
}
```

## 🚀 Running Both Applications

### Terminal 1: Backend Server
```bash
cd /path/to/little-lemon-restaurant
source littlelemon_env/bin/activate
python manage.py runserver
# Backend will run on http://127.0.0.1:8000
```

### Terminal 2: Frontend Server
```bash
cd /path/to/little-lemon-frontend
npm start
# or
yarn dev
# Frontend will typically run on http://localhost:3000
```

## 📡 Available API Endpoints

### Authentication
- `POST /api/token/` - Login and get JWT tokens
- `POST /api/token/refresh/` - Refresh access token

### Menu Management
- `GET /restaurant/menu/` - List all menu items (public)
- `GET /restaurant/menu/featured/` - Get featured items
- `GET /restaurant/menu/categories/` - Get all categories
- `GET /restaurant/menu/category/{category}/` - Get items by category
- `POST /restaurant/menu/` - Create menu item (authenticated)

### Booking System
- `GET /restaurant/booking/` - List user's bookings (authenticated)
- `POST /restaurant/booking/` - Create booking (authenticated)
- `GET /restaurant/booking/{id}/` - Get specific booking (authenticated)

### User Profile
- `GET /restaurant/profile/` - Get user profile (authenticated)

### Helper Endpoints
- `GET /restaurant/` - API overview and available endpoints

## 🛠 Common Frontend Modifications Needed

### 1. Authentication State Management

**React with Context:**
```javascript
// AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));

  useEffect(() => {
    if (token) {
      // Fetch user profile
      fetchUserProfile(token).then(setUser);
    }
  }, [token]);

  const login = async (username, password) => {
    // Implementation from Step 3 above
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

### 2. API Service Layer

```javascript
// services/api.js
const API_BASE = 'http://127.0.0.1:8000';

class ApiService {
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');

    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      ...options,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, config);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  // Menu methods
  getMenuItems() {
    return this.request('/restaurant/menu/');
  }

  getFeaturedItems() {
    return this.request('/restaurant/menu/featured/');
  }

  getMenuCategories() {
    return this.request('/restaurant/menu/categories/');
  }

  // Booking methods
  getUserBookings() {
    return this.request('/restaurant/booking/');
  }

  createBooking(bookingData) {
    return this.request('/restaurant/booking/', {
      method: 'POST',
      body: JSON.stringify(bookingData),
    });
  }

  // Auth methods
  login(username, password) {
    return this.request('/api/token/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }
}

export default new ApiService();
```

### 3. Component Updates

**Menu Component Example:**
```javascript
// components/Menu.js
import React, { useState, useEffect } from 'react';
import ApiService from '../services/api';

function Menu() {
  const [menuItems, setMenuItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    loadMenuData();
  }, []);

  const loadMenuData = async () => {
    try {
      const [menuResponse, categoriesResponse] = await Promise.all([
        ApiService.getMenuItems(),
        ApiService.getMenuCategories()
      ]);

      setMenuItems(menuResponse.results);
      setCategories(categoriesResponse);
    } catch (error) {
      console.error('Error loading menu:', error);
    }
  };

  const filteredItems = selectedCategory
    ? menuItems.filter(item => item.category === selectedCategory)
    : menuItems;

  return (
    <div className="menu">
      <div className="category-filter">
        <button onClick={() => setSelectedCategory('')}>All</button>
        {categories.map(category => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="menu-items">
        {filteredItems.map(item => (
          <div key={item.id} className="menu-item">
            <h3>{item.name}</h3>
            <p>{item.description}</p>
            <span className="price">${item.price}</span>
            {item.featured && <span className="featured">Featured</span>}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Menu;
```

## 🔧 Troubleshooting

### CORS Issues
If you encounter CORS errors:
1. Ensure the frontend URL is in `CORS_ALLOWED_ORIGINS`
2. Check that `CORS_ALLOW_ALL_ORIGINS = True` is set (development only)
3. Verify CORS middleware is properly configured

### Authentication Issues
1. Check token format: `Authorization: Bearer <token>`
2. Verify token is not expired (60-minute lifetime)
3. Use refresh token to get new access token

### API Response Format
Our API uses DRF pagination:
```javascript
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [...] // Your actual data is here
}
```

## 📱 Testing the Integration

### 1. Backend Test (Terminal 1)
```bash
# Test API is working
curl http://127.0.0.1:8000/restaurant/

# Test authentication
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Frontend Test (Browser)
1. Open browser to frontend URL (usually http://localhost:3000)
2. Check browser console for CORS or API errors
3. Test menu loading and authentication flow

## 🎯 Integration Checklist

- [ ] Frontend repository cloned and dependencies installed
- [ ] API base URL configured in frontend
- [ ] Authentication service updated for JWT
- [ ] Menu component updated to use backend API
- [ ] Booking component updated to use backend API
- [ ] Error handling implemented
- [ ] Both servers running simultaneously
- [ ] CORS configuration working
- [ ] Authentication flow working
- [ ] Data loading from backend successfully

## 🌟 Enhancements You Can Add

1. **Real-time Updates**: WebSocket integration for live booking updates
2. **Image Upload**: Add image fields to menu items
3. **Search Functionality**: Add search endpoints and frontend search
4. **Admin Dashboard**: Frontend admin interface for staff
5. **Email Notifications**: Booking confirmation emails
6. **Payment Integration**: Stripe/PayPal for reservations

## 🤝 Collaboration Tips

1. **Git Workflow**: Create a combined repository or use submodules
2. **Environment Variables**: Document all required environment variables
3. **Docker**: Consider containerizing both frontend and backend
4. **Testing**: Add integration tests for the full stack
5. **Deployment**: Deploy both to the same platform (Heroku, Vercel, etc.)

---

**Happy Full-Stack Development!** 🚀

Your Little Lemon Restaurant application will be an impressive portfolio piece showcasing both frontend and backend skills!
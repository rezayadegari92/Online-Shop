<div align="center">

# 🛒 Online Shop

### A Modern E-Commerce Platform Built with Django & Vue.js

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D.svg)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC.svg)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

*A full-featured e-commerce solution with modern architecture, real-time cart functionality, and seamless user experience.*

</div>

---

## ✨ Features

### 🛍️ **Product Management**
- **Rich Product Catalog** with high-quality images and detailed descriptions
- **Smart Categorization** with hierarchical category system
- **Brand Management** with logo support and brand-specific filtering
- **Dynamic Pricing** with discount system and promotional offers
- **Advanced Search** with filters, sorting, and pagination
- **Product Ratings** and review system

### 🛒 **Shopping Experience**
- **Real-time Cart** with instant updates and persistent storage
- **Guest Checkout** with session-based cart for anonymous users
- **Seamless Login Flow** with automatic cart merging
- **Smart Checkout Process** with address management and order confirmation
- **Order Tracking** with detailed order history and status updates

### 👤 **User Management**
- **Secure Authentication** with JWT tokens and refresh mechanism
- **Profile Management** with editable user information
- **Address Book** with CRUD operations and default address selection
- **Order History** with comprehensive order details and tracking
- **Responsive Design** optimized for all devices

### 🎨 **Modern UI/UX**
- **Beautiful Interface** built with Tailwind CSS
- **Interactive Components** powered by Vue.js 3
- **Real-time Updates** with reactive state management
- **Smooth Animations** and loading states
- **Mobile-First Design** with responsive breakpoints

---

## 🏗️ Architecture

<div align="center">

```mermaid
graph TB
    subgraph "Frontend (Vue.js 3)"
        A[Home Page] --> B[Product Catalog]
        B --> C[Product Details]
        C --> D[Shopping Cart]
        D --> E[Checkout Process]
        E --> F[Order Confirmation]
        
        G[User Authentication] --> H[Profile Management]
        H --> I[Address Management]
        H --> J[Order History]
    end
    
    subgraph "Backend (Django REST)"
        K[API Gateway] --> L[Authentication Service]
        K --> M[Product Service]
        K --> N[Cart Service]
        K --> O[Order Service]
        K --> P[User Service]
    end
    
    subgraph "Database Layer"
        Q[(PostgreSQL)]
        R[(Redis Cache)]
    end
    
    A -.-> K
    B -.-> M
    D -.-> N
    E -.-> O
    G -.-> L
    H -.-> P
    
    K --> Q
    K --> R
```

</div>

---

## 🛠️ Tech Stack

### **Backend Technologies**
<table>
<tr>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="40" height="40"/>
<br/><b>Django 4.2</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40"/>
<br/><b>Python 3.10</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" height="40"/>
<br/><b>PostgreSQL</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg" width="40" height="40"/>
<br/><b>Redis</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="40" height="40"/>
<br/><b>Docker</b>
</td>
</tr>
</table>

### **Frontend Technologies**
<table>
<tr>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg" width="40" height="40"/>
<br/><b>Vue.js 3</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="40" height="40"/>
<br/><b>TypeScript</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-plain.svg" width="40" height="40"/>
<br/><b>Tailwind CSS</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vitejs/vitejs-original.svg" width="40" height="40"/>
<br/><b>Vite</b>
</td>
<td align="center" width="20%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg" width="40" height="40"/>
<br/><b>Nginx</b>
</td>
</tr>
</table>

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Git

### **Option 1: Docker Setup (Recommended)**

```bash
# Clone the repository
git clone https://github.com/yourusername/online-shop.git
cd online-shop

# Start all services with Docker Compose
docker-compose up -d

# Populate database with sample data
docker-compose exec web python manage.py populate_products

# Create admin user
docker-compose exec web python manage.py createsuperuser
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

### **Option 2: Local Development**

```bash
# Backend Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py populate_products
python manage.py createsuperuser
python manage.py runserver

# Frontend Setup (in another terminal)
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure

```
online-shop/
├── 📁 accounts/                 # User authentication & management
│   ├── api/                    # REST API endpoints
│   ├── models.py               # User models
│   └── views.py                # Authentication views
├── 📁 products/                # Product management
│   ├── api/                    # Product API endpoints
│   ├── models.py               # Product, Category, Brand models
│   └── management/             # Django management commands
├── 📁 carts/                   # Shopping cart functionality
│   ├── api/                    # Cart API endpoints
│   ├── models.py               # Cart models
│   └── middleware.py           # Cart middleware
├── 📁 orders/                  # Order management
│   ├── api/                    # Order API endpoints
│   └── models.py               # Order models
├── 📁 addresses/               # Address management
│   ├── api/                    # Address API endpoints
│   └── models.py               # Address models
├── 📁 frontend/                # Vue.js frontend
│   ├── src/
│   │   ├── components/         # Reusable Vue components
│   │   ├── views/              # Page components
│   │   ├── stores/             # Pinia state management
│   │   └── utils/              # Utility functions
│   └── package.json            # Frontend dependencies
├── 📁 core/                    # Django project settings
│   ├── settings.py             # Main settings
│   └── urls.py                 # URL configuration
├── 📄 docker-compose.yml       # Docker services configuration
├── 📄 Dockerfile               # Backend container
└── 📄 requirements.txt         # Python dependencies
```

---

## 🔌 API Documentation

### **Authentication Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/accounts/api/register/` | User registration |
| `POST` | `/accounts/api/login/` | User login |
| `POST` | `/accounts/api/logout/` | User logout |
| `GET` | `/accounts/api/profile/` | Get user profile |
| `PATCH` | `/accounts/api/profile/` | Update user profile |

### **Product Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products/` | List all products |
| `GET` | `/api/products/{id}/` | Get product details |
| `GET` | `/api/categories/` | List categories |
| `GET` | `/api/brands/` | List brands |
| `GET` | `/api/discounted-products/` | Get discounted products |

### **Cart Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/cart/` | Get cart contents |
| `POST` | `/api/cart/` | Add item to cart |
| `PUT` | `/api/cart/{id}/` | Update cart item |
| `DELETE` | `/api/cart/{id}/` | Remove cart item |

### **Order Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/orders/` | List user orders |
| `POST` | `/api/orders/` | Create new order |
| `GET` | `/api/orders/{id}/` | Get order details |

---

## 🎯 Key Features in Detail

### **🛒 Smart Cart System**
- **Anonymous Cart**: Cookie-based storage for guest users
- **User Cart**: Database persistence for logged-in users
- **Cart Merging**: Automatic merge when user logs in
- **Real-time Updates**: Instant cart updates across the application

### **🔐 Advanced Authentication**
- **JWT Tokens**: Secure token-based authentication
- **Token Refresh**: Automatic token renewal
- **Session Management**: Secure session handling
- **Profile Management**: Complete user profile editing

### **📦 Order Management**
- **Checkout Process**: Multi-step checkout with validation
- **Address Management**: Full CRUD operations for addresses
- **Order Tracking**: Complete order history and status
- **Payment Integration**: Ready for payment gateway integration

### **🎨 Modern UI Components**
- **Responsive Design**: Mobile-first approach
- **Interactive Elements**: Smooth animations and transitions
- **Loading States**: User-friendly loading indicators
- **Error Handling**: Graceful error management

---

## 🧪 Testing

```bash
# Run backend tests
python manage.py test

# Run frontend tests
cd frontend
npm run test

# Run with coverage
npm run test:coverage
```

---

## 📊 Performance Features

- **Database Optimization**: Efficient queries with select_related and prefetch_related
- **Caching**: Redis-based caching for improved performance
- **Image Optimization**: Automatic image resizing and compression
- **Lazy Loading**: On-demand component loading
- **CDN Ready**: Optimized for content delivery networks

---

## 🔧 Configuration

### **Environment Variables**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/onlineshop

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=604800

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### **Development Guidelines**
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/TypeScript
- Write tests for new features
- Update documentation as needed

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists
- [Vue.js](https://vuejs.org/) - The progressive JavaScript framework
- [Tailwind CSS](https://tailwindcss.com/) - A utility-first CSS framework
- [Docker](https://docker.com/) - Containerization platform
- [Font Awesome](https://fontawesome.com/) - The web's most popular icon set

---

<div align="center">

### **⭐ Star this repository if you found it helpful!**

**Built with ❤️ by [Your Name]**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/yourusername)

</div>

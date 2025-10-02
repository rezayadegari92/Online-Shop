# Online Shop

A modern e-commerce platform built with Django and Vue.js, featuring a responsive design and real-time cart functionality.

## Features

- 🛍️ **Product Management**
  - Product listings with images, prices, and descriptions
  - Category and brand organization
  - Discount system
  - Product ratings and reviews
  - Search functionality
  - Filtering and sorting options

- 🛒 **Shopping Cart**
  - Real-time cart updates
  - Persistent cart for logged-in users
  - Session-based cart for guests
  - Quantity management
  - Price calculations with discounts

- 👤 **User Management**
  - User registration and authentication
  - Profile management
  - Order history
  - Wishlist functionality

- 🎨 **Modern UI/UX**
  - Responsive design using Tailwind CSS
  - Interactive components with Vue.js
  - Real-time updates
  - Loading states and animations
  - Toast notifications

## Tech Stack

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Django CORS Headers

### Frontend
- Vue.js 3
- Tailwind CSS
- Axios for API calls
- Font Awesome icons

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/online-shop.git
cd online-shop
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
online-shop/
├── accounts/          # User authentication and management
├── cart/             # Shopping cart functionality
├── products/         # Product management
├── pages/            # Main pages and views
├── templates/        # HTML templates
│   ├── accounts/     # Authentication templates
│   ├── cart/         # Cart templates
│   └── products/     # Product templates
├── static/           # Static files (CSS, JS, images)
└── online_shop/      # Project settings
```

## API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<id>/` - Get product details
- `GET /api/categories/` - List all categories
- `GET /api/brands/` - List all brands
- `GET /api/top-rated/` - Get top-rated products
- `GET /api/discounts/` - Get discounted products

### Cart
- `GET /api/cart/` - Get cart contents
- `POST /api/cart/` - Add item to cart
- `PUT /api/cart/` - Update cart item quantity
- `DELETE /api/cart/` - Remove item from cart

### Authentication
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Vue.js](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings - Use environment variables
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-u=fu0qz87^zgchrjaug-1(0l9@!b^1sykjs)s13^nk&&2-&pty"
)

DEBUG = os.getenv("DEBUG", "1") in ("1", "True", "true", "yes")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django_prometheus",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local apps
    "apps.accounts.apps.AccountsConfig",
    "apps.products.apps.ProductsConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.addresses.apps.AddressesConfig",
    "core.apps.CoreConfig",
    "apps.carts.apps.CartsConfig",
    "apps.wishlists.apps.WishlistsConfig",
    "drf_spectacular",
    # third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.carts.middleware.CartMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database configuration - uses individual environment variables
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "onlineshop"),
        "USER": os.getenv("POSTGRES_USER", "onlineshop"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "onlineshop"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": int(os.getenv("POSTGRES_PORT", "5432")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = (
    [os.path.join(BASE_DIR, "static")]
    if os.path.exists(os.path.join(BASE_DIR, "static"))
    else []
)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Ensure media directory exists
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    # 'accounts.authentication.EmailOrUsernameModelBackend',
    "django.contrib.auth.backends.ModelBackend",
]

# 📨 Email Configuration - Use environment variables
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "yadegarireza50@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "neks hzfr ymul thln")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# 🔐 Login redirect paths
# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/login/'

# 🔐 DRF + JWT
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # Allow anonymous access by default
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # Set default page size
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Online Shop API",
    "DESCRIPTION": "API for an online shop built with Django Rest Framework",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [{"jwtAuth": []}],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "jwtAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT access token (without Bearer prefix)",
            }
        }
    },
    "PREPROCESSING_HOOKS": ["drf_spectacular.hooks.preprocess_exclude_path_format"],
    "POSTPROCESSING_HOOKS": [],
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", "45"))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_LIFETIME_DAYS", "1"))
    ),
    "ROTATE_REFRESH_TOKENS": os.getenv("JWT_ROTATE_REFRESH_TOKENS", "True") == "True",
    "BLACKLIST_AFTER_ROTATION": os.getenv("JWT_BLACKLIST_AFTER_ROTATION", "True")
    == "True",
}

# 🐇 Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 10

# 🗄️ Redis Cache Configuration
# REDIS_URL format: redis://:password@host:port/db or redis://username:password@host:port/db
# Alternatively, build from components: REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    # Build Redis URL from components if REDIS_URL is not provided
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT", "6379")
    redis_password = os.getenv("REDIS_PASSWORD")
    redis_db = os.getenv("REDIS_DB", "1")
    
    if redis_host:
        if redis_password:
            redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
        else:
            redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"

if redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {
                    "max_connections": 50,
                    "retry_on_timeout": True,
                },
                "SOCKET_CONNECT_TIMEOUT": 5,
                "SOCKET_TIMEOUT": 5,
            },
            "KEY_PREFIX": "onlineshop",
            "TIMEOUT": 300,  # Default timeout: 5 minutes
        }
    }
else:
    # Fallback to dummy cache if REDIS_URL is not set
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

# Cache time settings (in seconds)
CACHE_TTL = {
    "PRODUCT_LIST": 60 * 10,  # 10 minutes
    "PRODUCT_DETAIL": 60 * 15,  # 15 minutes
    "CATEGORY_LIST": 60 * 30,  # 30 minutes
    "CATEGORY_PRODUCTS": 60 * 10,  # 10 minutes
    "BRAND_LIST": 60 * 30,  # 30 minutes
    "BRAND_PRODUCTS": 60 * 10,  # 10 minutes
    "TOP_RATED": 60 * 15,  # 15 minutes
    "DISCOUNTED": 60 * 10,  # 10 minutes
}

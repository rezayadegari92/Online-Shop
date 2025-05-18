from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # Include pages app URLs at root
    path('users/', include('users.urls')),  # Include users app URLs
    path('api/products/', include('products.api.urls')),
    path('api/cart/', include('carts.api.urls')),
    path('api/orders/', include('orders.api.urls')),
    path('api/users/', include('users.api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
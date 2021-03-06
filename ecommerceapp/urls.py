"""ecommerceapp URL Configuration
"""

# From django
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/carts/', include('carts.urls')),
    path('api/v1/purchases/', include('purchases.urls'))
]

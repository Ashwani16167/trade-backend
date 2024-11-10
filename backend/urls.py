from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trades.urls')),
    path('api/', include('trades.urls')),
]

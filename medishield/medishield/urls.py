from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', include('pharma.urls')),  # Include URLs from the 'pharma' app
]

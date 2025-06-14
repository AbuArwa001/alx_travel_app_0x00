"""
URL configuration for alx_travel_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from listings.views import (
    PropertyViewSet, BookingViewSet, PaymentViewSet, ReviewViewSet, MessageViewSet
)

from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'properties', PropertyViewSet, basename='property')
routers.register(r'bookings', BookingViewSet, basename='booking')
routers.register(r'payments', PaymentViewSet, basename='payment')
routers.register(r'reviews', ReviewViewSet, basename='review')
routers.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', RedirectView.as_view(url='/api/docs/')),
]

urlpatterns += routers.urls
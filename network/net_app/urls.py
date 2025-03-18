from django.urls import path

from .views import ipv4_test_view

urlpatterns = [
    path('ipv4/', ipv4_test_view),
]

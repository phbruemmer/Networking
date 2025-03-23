from django.urls import path

from .views import ipv4_test_view, link_local_test_view

urlpatterns = [
    path('ipv4/', ipv4_test_view),
    path('ipv6/', link_local_test_view),
]

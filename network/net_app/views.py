from django.shortcuts import render


def ipv4_test_view(request):
    return render(request, "ipv4.html")


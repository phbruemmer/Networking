from django.shortcuts import render

from .prvt_modules.custom import Network


def ipv4_test_view(request):
    input_fields = {
        "network_address": None,
        "host_portions": None,
        "broadcast_address": None,
        "max_hosts": None,
        "address_range_from": None,
        "address_range_to": None,
    }
    network = Network()
    network.create_random_ip_from_subnet()

    args = {
        'IP': network.ip,
        'SUBNETMASK': network.subnet_mask,
    }

    if request.method == 'POST':
        for field in input_fields:
            input_fields[field] = request.POST.get(field)
        print(input_fields)
    return render(request, "ipv4.html", args)


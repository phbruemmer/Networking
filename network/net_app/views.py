from Scripts.bottle import redirect
from django.shortcuts import render

from .prvt_modules.custom import Network
from .prvt_modules.network_checks import check_data


def ipv4_test_view(request):
    input_fields = {
        "ip": None,
        "subnet_mask": None,
        "network_address": None,
        "host_portions": None,
        "broadcast_address": None,
        "max_hosts": None,
        "address_range_from": None,
        "address_range_to": None,
    }
    network = Network()

    if request.method == 'POST':
        for field in input_fields:
            input_fields[field] = request.POST.get(field)

        network.ip = input_fields["ip"]
        network.subnet_mask = input_fields["subnet_mask"]
        network.check_values()
        network.create_dict()

        correct_data = check_data(input_fields, network.dict)
    else:
        network.create_random_ip_from_subnet()

    args = {
        'IP': network.ip,
        'SUBNET_MASK': network.subnet_mask,
    }

    return render(request, "ipv4.html", args)

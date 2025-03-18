from django.shortcuts import render
from .prvt_modules.custom import Network
from .prvt_modules.network_checks import check_data


def ipv4_test_view(request):
    def process_inputs():
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

        for field in input_fields:
            print(field)
            if field is None:
                return
            input_fields[field] = request.POST.get(field)
        network.ip = input_fields["ip"]
        network.subnet_mask = input_fields["subnet_mask"]

        network.check_values()
        network.create_dict()

        correct_data = check_data(input_fields, network.dict)
        correct_data.pop(0)
        correct_data.pop(0)
        args['correct_data'] = correct_data

    args = {}

    network = Network()

    if request.method == 'POST':
        btn_action = request.POST.get('action')
        if btn_action == 'check':
            process_inputs()
        elif btn_action == 'next':
            network.create_subnet_mask()
            network.create_random_ip_from_subnet()
        else:
            args.update({
                'IP': "Invalid Input - Try again!"
            })
    else:
        network.create_random_ip_from_subnet()

    args.update({
        'IP': network.ip,
        'SUBNET_MASK': network.subnet_mask,
    })

    return render(request, "ipv4.html", args)

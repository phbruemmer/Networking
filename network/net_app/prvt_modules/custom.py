import random
import ipaddress


def create_random_ip():
    return f"{random.randrange(1, 224)}.{random.randrange(1, 224)}.{random.randrange(1, 224)}.{random.randrange(1, 224)}"


class Network:
    def __init__(self):
        self.ip = None
        self.subnet_mask = None

        self.broadcast_address = None
        self.network_address = None
        self.host_portions = None
        self.first_ip = None
        self.last_ip = None
        self.hosts = None

    def edge_case(self):
        self.ip = None
        self.subnet_mask = None

        self.broadcast_address = None
        self.network_address = None
        self.host_portions = None
        self.first_ip = None
        self.last_ip = None
        self.hosts = None

    def create_subnet_mask(self):
        prefix_length = random.randint(8, 32)
        binary_mask = "1" * prefix_length + "0" * (32 - prefix_length)

        subnet_mask = []
        for i in range(0, 32, 8):
            subnet_mask.append(str(int(binary_mask[i: i + 8], 2)))

        self.subnet_mask = ".".join(subnet_mask)
        return self.subnet_mask

    def create_random_ip_from_subnet(self):
        if self.subnet_mask is None:
            self.create_subnet_mask()

        private_network_ranges = [
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16"
        ]

        try:
            selected_network = random.choice(private_network_ranges)

            network_with_mask = f"{selected_network.split('/')[0]}/{self.subnet_mask}"

            net = ipaddress.IPv4Network(network_with_mask, strict=False)

            network_address = net.network_address
            broadcast_address = net.broadcast_address

            first_usable_ip = network_address + 1
            last_usable_ip = broadcast_address - 1

            first_usable_ip_int = int(first_usable_ip)
            last_usable_ip_int = int(last_usable_ip)

            random_ip_int = random.randint(min(first_usable_ip_int, last_usable_ip_int),
                                           max(first_usable_ip_int, last_usable_ip_int))
        except Exception as e:
            self.edge_case()
            raise e

        self.ip = str(ipaddress.IPv4Address(random_ip_int))
        return self.ip

    def calculate_host_portions(self):
        # divides the address into 4 parts and turns each octet into an integer in a new list
        separated_subnet_mask_int = [~int(octet) for octet in self.subnet_mask.split('.')]
        separated_ip_int = [int(octet) for octet in self.ip.split('.')]

        # iterates through both the subnet_mask and ip lists,
        # performs a bitwise AND operation on each corresponding
        # octet, and stores the result.
        self.host_portions = '.'.join([str(separated_subnet_mask_int[i] & separated_ip_int[i]) for i in range(0, 4)])
        return self.host_portions

    def check_values(self):
        network_mask = f"{self.ip}/{self.subnet_mask}"
        net = ipaddress.IPv4Network(network_mask, strict=True)

        self.network_address = net.network_address
        self.broadcast_address = net.broadcast_address

        self.calculate_host_portions()

        self.first_ip = self.network_address + 1
        self.last_ip = self.broadcast_address - 1

    def calc_max_number_of_hosts(self):
        subnet_mask = '.'.join([bin(int(octet))[2:].zfill(8) for octet in self.subnet_mask.split('.')])
        self.hosts = (2 ** subnet_mask.count('0')) - 2
        return self.hosts


if __name__ == '__main__':
    network = Network()
    network.subnet_mask = "255.255.192.0"
    network.calc_max_number_of_hosts()

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

        self.dict = {}

    def edge_case(self):
        self.ip = None
        self.subnet_mask = None

        self.broadcast_address = None
        self.network_address = None
        self.host_portions = None
        self.first_ip = None
        self.last_ip = None
        self.hosts = None

        self.dict = {}

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
        separated_subnet_mask_int = [255 - int(octet) for octet in self.subnet_mask.split('.')]
        separated_ip_int = [int(octet) for octet in self.ip.split('.')]
        self.host_portions = '.'.join([str(separated_subnet_mask_int[i] & separated_ip_int[i]) for i in range(4)])
        return self.host_portions

    def check_values(self):
        network_mask = f"{self.ip}/{self.subnet_mask}"
        print(network_mask)
        net = ipaddress.IPv4Network(network_mask, strict=False)

        self.network_address = net.network_address
        self.broadcast_address = net.broadcast_address

        self.calculate_host_portions()
        self.calc_max_number_of_hosts()

        self.first_ip = self.network_address + 1
        self.last_ip = self.broadcast_address - 1

    def calc_max_number_of_hosts(self):
        subnet_mask = '.'.join([bin(int(octet))[2:].zfill(8) for octet in self.subnet_mask.split('.')])
        self.hosts = (2 ** subnet_mask.count('0')) - 2
        return self.hosts

    def create_dict(self):
        self.dict = {
            "ip": self.ip,
            "subnet_mask": self.subnet_mask,
            "network_address": self.network_address,
            "host_portions": self.host_portions,
            "broadcast_address": self.broadcast_address,
            "max_hosts": self.hosts,
            "address_range_from": self.first_ip,
            "address_range_to": self.last_ip,
        }
        return self.dict


class Ipv6:
    def __init__(self):
        self.ipv6 = None
        self.MAC = None

    def create_MAC(self):
        self.MAC = ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))
        return self.MAC

    def create_random(self):
        self.ipv6 = str(ipaddress.IPv6Address(random.getrandbits(128)))
        return self.ipv6

    def create_private(self):
        prefix = "fd"
        rest = ":".join(f"{random.randint(0, 65535):x}" for _ in range(7))
        self.ipv6 = f"{prefix}00::{rest}"
        return self.ipv6

    def create_link_local(self):
        prefix = "FE80:" + ":".join(["0" * 4] * 3)
        suffix = ":".join(f"{random.randint(0, 65535):04x}" for _ in range(4))
        self.ipv6 = f"{prefix}:{suffix}"
        return self.ipv6

    def create_link_local_based_on_mac(self):
        if self.MAC is None:
            self.create_MAC()
        split_mac = self.MAC.split(':')
        prefix = "fe80:" + ":".join(["0" * 4] * 3)
        ### merge two byte segments and add ff:fe into the center ###
        split_mac[2] += "ff"
        split_mac[3] = "fe" + split_mac[3]
        split_mac[4] += split_mac[5]
        split_mac.pop(5)
        ### calculate full suffix ###
        suffix = f"{(int(split_mac[0], 16) ^ 0x02):02x}" + ":".join(split_mac[1:])

        self.ipv6 = f"{prefix}:{suffix}"
        return self.ipv6

    def check_ipv6(self):
        if self.ipv6 is None:
            raise ValueError("No ipv6 address given!")

        split_ip = self.ipv6.split(':')
        ip_size = len(split_ip)
        double_colons = self.ipv6.count('::')

        if ip_size == 1 or double_colons > 1:
            return False

        prev_char = ""
        consecutive_colons = 0

        for char in self.ipv6:
            if prev_char == ":" and char == ":":
                consecutive_colons += 1
                if consecutive_colons > 1:
                    return False
            prev_char = char

        if double_colons == 0 and not ip_size == 8:
            return False
        elif double_colons == 1 and (not ip_size <= 8 or not ip_size > 1):
            return False

        for segment in split_ip:
            if segment == "":
                continue
            try:
                if not (0 <= int(segment, 16) <= 65535):
                    return False
            except ValueError:
                return False
        return True

    def get_full_length(self):
        if self.ipv6 is None:
            raise ValueError("No ipv6 address given!")
        if not self.check_ipv6():
            return

        split_addr = []
        prev_char = ""
        temp = ""

        for char in self.ipv6:
            if char == ":":
                if temp != "":
                    split_addr.append(f"{int(temp, 16):04x}")
                    temp = ""
            else:
                temp += char
            if prev_char == ":" and char == ":":
                split_addr.append("")
            prev_char = char
        split_addr.append(temp)

        for segment_iter in range(0, len(split_addr)):
            if split_addr[segment_iter] == "":
                iter = segment_iter
                split_addr.pop(segment_iter)
                for i in range(0, 8 - len(split_addr)):
                    split_addr.insert(iter, "0" * 4)
                    iter += 1
        self.ipv6 = ':'.join(split_addr)
        return self.ipv6


if __name__ == '__main__':
    ipv6 = Ipv6()
    ipv6.ipv6 = "2001:db8:85a3::8a2e:370:7334"
    print(ipv6.get_full_length())

import subprocess
from getmac import get_mac_address
from decouple import config, Csv


class MACHandler:

    def __init__(self):
        self.mac_list = set(config("MAC_ADDRESSES", cast=Csv()))

    def check_network(self):
        count = 1
        discovered_devices = []
        network_scan = subprocess.Popen(["nmap -sn 192.168.0.0/24"], shell=True, stdout=subprocess.PIPE)
        with network_scan.stdout as scan:
            for line in scan:
                if count % 2 == 0:
                    try:
                        discovered_devices.append(line.decode("utf-8").strip("\n").split()[5])
                    except IndexError:
                        print("Error fetching details of device")
                count += 1
        discovered_devices.pop()
        discovered_devices = set([get_mac_address(ip=i[1:len(i)-1]) for i in discovered_devices])
        if None in discovered_devices:
            discovered_devices.remove(None)
        if self.mac_list.intersection(discovered_devices).__len__() == 0:
            return True
        else:
            return False


print(MACHandler().check_network())
import subprocess
from getmac import get_mac_address
from decouple import config, Csv
import logging


class MACHandler:

    def __init__(self):
        self.mac_list = set(config("MAC_ADDRESSES", cast=Csv()))

    def check_network(self):
        count = 1
        discovered_devices = []
        logging.debug("Scanning network for connected devices...")
        network_scan = subprocess.Popen(["nmap -sn 192.168.0.0/24"], shell=True, stdout=subprocess.PIPE)
        with network_scan.stdout as scan:
            for line in scan:
                if count % 2 == 0:
                    try:
                        discovered_devices.append(line.decode("utf-8").strip("\n").split()[5])
                    except IndexError:
                        discovered_devices.append(line.decode("utf-8").strip("\n").split()[4])
                count += 1
        discovered_devices.pop()
        logging.debug("Converting IP addresses to MAC addresses...")
        discovered_devices = set([get_mac_address(ip=i.strip(")").strip("(")) for i in discovered_devices])
        if None in discovered_devices:
            discovered_devices.remove(None)
        device_intersection_cardinality = self.mac_list.intersection(discovered_devices).__len__()
        if device_intersection_cardinality == 0:
            logging.info("No necessary devices connected to network.")
            return True
        else:
            logging.info("%d devices connected to the network." % device_intersection_cardinality)
            return False

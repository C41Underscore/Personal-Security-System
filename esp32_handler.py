from PIL import Image
import urllib.request
from string import Template
from time_handler import get_formatted_time
import socket


class ESP32CamInterface:

    template_url = Template("http://${ip_address}/${image_type}")

    def __init__(self, cam_num, ip_address, location, cam_socket=None):
        self.id = cam_num
        self.ip_address = ip_address
        self.location = location

    def __str__(self):
        return "Camera: %d, IP address: %s, Location: %s" % (self.id, self.ip_address, self.location)

    def take_image(self, high_quality):
        current_time = get_formatted_time(False)
        if high_quality:
            image = Image.open(urllib.request.urlopen(ESP32CamInterface.template_url.substitute(
                ip_address=self.ip_address,
                image_type="cam-hi.jpg"
            )))
        else:
            image = Image.open(urllib.request.urlopen(ESP32CamInterface.template_url.substitute(
                ip_address=self.ip_address,
                image_type="cam-lo.jpg"
            )))
        return image, current_time


class CameraCollection:

    def __init__(self, *camera_interface_details):
        self.is_active = False
        self.camera_interfaces = []
        for i, details in enumerate(camera_interface_details):
            self.camera_interfaces.append(ESP32CamInterface(i+1, details[0], details[1]))

    def activate_cams(self):
        self.is_active = True

    def check_cams(self):
        pass



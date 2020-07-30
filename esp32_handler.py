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
        #self.cam_socket = cam_socket
        #self.cam_socket.setBlocking(False)
        self.active = False

    def take_image(self, high_quality):
        current_time = get_formatted_time(False)
        # image = Image.open(urllib.request.urlopen(ESP32CAM_Interface.template_url.substitute(
        #     ip_address=self.ip_address,
        #     image_type=("cam-hi.jpg" if high_quality else "cam-lo.jpg")
        # )))
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

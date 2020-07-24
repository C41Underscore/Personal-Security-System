from PIL import Image
import urllib.request
from string import Template

class ESP32CAM_Interface:

    template_url = Template("http://${ip_address}/${image_type}")

    def __init__(self, cam_num, ip_address, location):
        self.id = cam_num
        self.ip_address = ip_address
        self.location = location

    def takeImage(self, high_quality):
        # image = Image.open(urllib.request.urlopen(ESP32CAM_Interface.template_url.substitute(
        #     ip_address=self.ip_address,
        #     image_type=("cam-hi.jpg" if high_quality else "cam-lo.jpg")
        # )))
        if high_quality:
            image = Image.open(urllib.request.urlopen(ESP32CAM_Interface.template_url.substitute(
                ip_address=self.ip_address,
                image_type="cam-hi.jpg"
            )))
        else:
            image = Image.open(urllib.request.urlopen(ESP32CAM_Interface.template_url.substitute(
                ip_address=self.ip_address,
                image_type="cam-lo.jpg"
            )))
        width, height = image.size
        print(width, height)

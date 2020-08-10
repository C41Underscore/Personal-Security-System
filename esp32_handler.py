from PIL import Image
import urllib.request
from string import Template
from time_handler import get_formatted_time
import socket
import logging


class ESP32CamInterface:

    template_url = Template("http://${ip_address}/${image_type}")

    def __init__(self, cam_num, ip_address, cam_socket=None):
        self.id = cam_num
        self.ip_address = ip_address
        self.cam_socket = cam_socket

    def __str__(self):
        return "Camera: %d, IP address: %s" % (self.id, self.ip_address)

    def take_image(self, high_quality):
        logging.debug("Taking image with camera %d, IP address %s" % (self.id, self.ip_address))
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
        logging.debug("Image quality: %s" % "High" if high_quality else "Low")
        return image, current_time

    def check_camera(self):
        data = self.cam_socket.recv(1024)
        if data.__len__() == 0:
            return None
        else:
            data = data.decode("utf-8")
            if data == "BITCHES DETECTED :0":
                logging.info("Camera %d detected movement, taking image now!" % self.id)

    def change_camera_state(self, new_state):
        self.cam_socket.send("Time to get snappy:triumph:" if new_state else "Behave!")


class CameraCollection:

    def __init__(self, number_of_cams):
        self.is_active = False
        self.camera_interfaces = []
        cur_no_cams = 0
        logging.debug("Creating listening socket.")
        connection_socket = socket.socket()
        host, port = ("0.0.0.0", 8080)
        logging.debug("Binding socket to address %s, on socket %d." % (host, port))
        connection_socket.bind((host, port))
        logging.debug("Listening for incoming requests.")
        connection_socket.listen()
        while True:
            cam_sock, cam_addr = connection_socket.accept()
            cur_no_cams += 1
            self.camera_interfaces.append(ESP32CamInterface(cur_no_cams, cam_addr[0], cam_sock))
            logging.info("Camera connected to with IP address %s" % cam_addr[0])
            if cur_no_cams == number_of_cams:
                break
        logging.debug("Closing listening socket.")
        connection_socket.close()

    def set_system_state(self, new_state):
        self.is_active = new_state
        for camera in self.camera_interfaces:
            camera.change_camera_state(new_state)
        logging.debug("CameraCollection.is_active=%s." % self.is_active)
        logging.info("System activated." if self.is_active else "System deactivated.")

    def check_cams(self):
        while True:
            if self.is_active:
                logging.info("Checking cameras for detected movement...")
                for camera in self.camera_interfaces:
                    camera.check_camera()


if __name__ == "__main__":
    cam_coll = CameraCollection(1)
    for _ in range(100):
        cam_coll.check_cams()

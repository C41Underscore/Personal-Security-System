from PIL import Image
import urllib.request
from string import Template
from time_handler import get_formatted_time
import socket
import logging
from google_drive_handler import DriveHandler
from http.client import IncompleteRead
from urllib.error import URLError
from multiprocessing import current_process


class ESP32CamInterface:

    template_url = Template("http://${ip_address}/${image_type}")

    def __init__(self, cam_num, ip_address, cam_socket=None):
        self.id = cam_num
        self.ip_address = ip_address
        self.cam_socket = cam_socket
        self.cam_socket.settimeout(10)

    def __str__(self):
        return "Camera: %d, IP address: %s" % (self.id, self.ip_address)

    def take_image(self, high_quality):
        logging.debug("Taking image with camera %d, IP address %s" % (self.id, self.ip_address))
        current_time = get_formatted_time(False)
        try:
            if high_quality:
                image = Image.open(urllib.request.urlopen(ESP32CamInterface.template_url.substitute(
                    ip_address=self.ip_address,
                    image_type="cam-hi.jpg"
                ), timeout=30))
            else:
                image = Image.open(urllib.request.urlopen(ESP32CamInterface.template_url.substitute(
                    ip_address=self.ip_address,
                    image_type="cam-lo.jpg"
                ), timeout=30))
            logging.debug("Image quality: %s" % ("High" if high_quality else "Low"))
        except (IncompleteRead, URLError) as e:
            logging.debug("Error whilst taking image: %s" % e)
            image = ""
        except socket.timeout as e:
            self.reconnect()
            image = ""
        return image, current_time

    def reconnect(self):
        self.cam_socket = socket.socket()
        logging.debug("No data obtained on camera %d, attempting to reconnect..." % self.id)
        self.cam_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = ("0.0.0.0", 8080)
        self.cam_socket.bind((host, port))
        self.cam_socket.listen()
        while True:
            cam_sock, cam_addr = self.cam_socket.accept()
            if cam_addr[0] == self.ip_address:
                self.cam_socket = cam_sock
                self.cam_socket.settimeout(10)
                break

    def check_camera(self):
        try:
            logging.debug("Checking camera %d on process %s" % (self.id, current_process().name))
            data = self.cam_socket.recv(1024).decode("utf-8")
            # logging.debug("Camera data obtained: %s" % data)
            if "1" in data:
                logging.info("Camera %d detected movement, taking image..." % self.id)
                return self.take_image(False)
        except socket.timeout as e:
            self.reconnect()
        return "", "Big Chungus"


class CameraCollection:

    def __init__(self, number_of_cams):
        self.is_active = False
        self.camera_interfaces = []
        connected_ip_addresses = set()
        cur_no_cams = 0
        logging.debug("Creating listening socket.")
        connection_socket = socket.socket()
        connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = ("0.0.0.0", 8080)
        logging.debug("Binding socket to address %s, on socket %d." % (host, port))
        connection_socket.bind((host, port))
        logging.debug("Listening for incoming requests...")
        connection_socket.listen()
        while cur_no_cams < number_of_cams:
            cam_sock, cam_addr = connection_socket.accept()
            if cam_addr not in connected_ip_addresses:
                cur_no_cams += 1
                self.camera_interfaces.append(ESP32CamInterface(cur_no_cams, cam_addr[0], cam_sock))
                logging.info("Camera connected to with IP address %s" % cam_addr[0])
        logging.debug("Closing listening socket.")
        connection_socket.close()

    def set_system_state(self, new_state):
        self.is_active = new_state
        logging.debug("CameraCollection.is_active=%s." % self.is_active)
        logging.info("System is on." if self.is_active else "System is off.")

    def camera_loop(self, drive, activation_q):
        while True:
            self.set_system_state(activation_q.get())
            if self.is_active:
                logging.info("Checking cameras for detected movement...")
                for camera in self.camera_interfaces:
                    try:
                        check_image, check_time = camera.check_camera()
                    except TypeError as e:
                        logging.error("Couldn't get image off camera!")
                        logging.error(e)
                        continue
                    if check_image != "":
                        logging.debug("Saving image to the drive...")
                        check_time += ".jpg"
                        check_image.save(check_time)
                        drive.upload(get_formatted_time(True), check_time)
            else:
                for camera in self.camera_interfaces:
                    try:
                        camera.cam_socket.sendall(b"9")
                    except socket.error as e:
                        print(e)
                        camera.reconnect()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    cam_coll = CameraCollection(1)
    cam_coll.is_active = True
    drive = DriveHandler()
    for _ in range(100):
        cam_coll.camera_loop(drive)

import google_drive_auth
import google_drive_upload
from esp32_handler import ESP32CAM_Interface


def main(testing):
    drive = google_drive_auth.authenticate()
    esp32cam = ESP32CAM_Interface(1, "${IP_ADDRESS}", "Living Room")
    if testing:
        for i in range(0, 10):
            esp32cam.takeImage(False)


if __name__ == "__main__":
    main(True)

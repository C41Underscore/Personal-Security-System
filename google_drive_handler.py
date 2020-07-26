from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)


def upload(drive, filename, filepath):
    file1 = drive.CreateFile({"title": filename})
    file1.SetContentFile(filepath)
    file1.Upload()


if __name__ == "__main__":
    upload()

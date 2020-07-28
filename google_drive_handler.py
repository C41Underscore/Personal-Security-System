from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def authenticate():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("google_credentials.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("google_credentials.txt")
    return GoogleDrive(gauth)


def upload(drive, filename, filepath):
    file1 = drive.CreateFile({"title": filename})
    file1.SetContentFile(filepath)
    file1.Upload()


if __name__ == "__main__":
    upload()

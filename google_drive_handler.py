from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from time_handler import get_formatted_time


class DriveHandler:

    def __init__(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("google_credentials.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile("google_credentials.txt")
        self.drive = GoogleDrive(gauth)

    def refresh_drive(self):
        pass

    def upload(self, directory, filename):
        folder_id = None
        folder_list = self.drive.ListFile(
            {"q": "title='%s' and mimeType='application/vnd.google-apps.folder' and trashed=false" % directory}

        ).GetList()
        for folder in folder_list:
            if folder["title"] == directory:
                folder_id = folder["id"]
                break
        if folder_id is None:
            directory = self.drive.CreateFile({"title": directory, "mimeType": "application/vnd.google-apps.folder"})
            directory.Upload()
            folder_id = directory["id"]
        new_file = self.drive.CreateFile({"title": filename, "parents": [{"id": folder_id}]})
        filename = "test-image.jpg"
        new_file.SetContentFile(filename)
        new_file.Upload()


DriveHandler().upload(get_formatted_time(True), get_formatted_time(False))

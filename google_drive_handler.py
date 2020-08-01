from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from time_handler import get_current_date
from datetime import timedelta


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

    def refresh_drive(self, current_date):
        folder_list = self.drive.ListFile(
            {"q": "mimeType='application/vnd.google-apps.folder' and trashed=true"}
        ).GetList()
        for folder in folder_list:
            folder_to_delete = self.drive.CreateFile({"id": folder["id"]})
            folder_to_delete.Delete()
        folders_to_trash = []
        date_modifier = timedelta(days=1)
        folder_list = self.drive.ListFile(
            {"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}
        ).GetList()
        for i in range(0, 5):
            current_date -= date_modifier
            date_str = current_date.__str__()
            for folder in folder_list:
                if folder["title"] == date_str:
                    folders_to_trash.append(folder["id"])
        for folder in folders_to_trash:
            folder = self.drive.CreateFile({"id": folder})
            folder.Trash()

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

import google_drive_auth

def upload():
    drive = google_drive_auth.authenticate()
    file1 = drive.CreateFile({"title":"test-image.jpg"})
    file1.SetContentFile("test-image.jpg")
    file1.Upload()


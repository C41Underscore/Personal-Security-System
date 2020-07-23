from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = "https://www.googleapis.com/auth/drive"

CREDENTIALS = "credentials.json"

store = file.Storage("storage.json")
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CREDENTIALS, SCOPES)
    creds = tools.run_flow(flow, store)

SERVICE = build("drive", "v3", http=creds.authorize(Http()))
print("Service end point created", SERVICE)

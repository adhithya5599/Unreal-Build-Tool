import os.path
import os
import shutil
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive.readonly"]

def create_zip(local_folder, zip_name):
    base_name = os.path.splitext(zip_name)[0]
    zip_path = shutil.make_archive(base_name, "zip", local_folder)
    return zip_path

def main(local_folder, drive_folder_id, zip_name):
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  token_path = r"C:\Users\u1475663\source\repos\Unreal-Auto-Build\app\token.json"
  cred_path = r"C:\Users\u1475663\source\repos\Unreal-Auto-Build\app\credentials.json"
  if os.path.exists(token_path):
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    except :
        pass 
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    try:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No valid credentials, regenerated token")
    except Exception:
        flow = InstalledAppFlow.from_client_secrets_file(
            cred_path, SCOPES
        )
        creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json()) 

  try:
    service = build("drive", "v3", credentials=creds)
    zip_path = create_zip(local_folder, zip_name)
    file_metada = {
        "name":os.path.basename(zip_path),
        "parents":[drive_folder_id]
    }
    response = service.files().list(
                                q=f"'{drive_folder_id}' in parents and name='{os.path.basename(zip_path)}'",
                                spaces="drive",
                                fields="files(id,name)",
                            ).execute()
    for file in response.get("files", []):
        print(f"Deleting old file: {file['name']} ({file['id']})")
        try :
            service.files().delete(fileId=file['id']).execute()
        except :
            print("Failed to delete old file")
            pass
    media = MediaFileUpload(zip_path, resumable=True)
    request = service.files().create(
                                body=file_metada,
                                media_body=media,
                                fields="id"
                            )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print(f"Upload Complete. File ID: {response.get('id')}")
    return response.get('id')

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")
  
if __name__ == "__main__":
  drive_folder_id = "1ZivDW9GnbjTnDhitT9ynq0SpxBAkg3Qy"
  local_folder = r"C:\Users\u1475663\source\UnrealTestBuilds"
  zip_name = "FarmHandsBuild.zip"
  main(local_folder, drive_folder_id, zip_name)
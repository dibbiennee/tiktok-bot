import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from config.settings import CREDENTIALS_FILE, TOKEN_FILE

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            json.dump(json.loads(creds.to_json()), token)
    return build('drive', 'v3', credentials=creds)


def list_videos(folder_id: str) -> list:
    try:
        service = get_drive_service()
        results = service.files().list(
            q=f"'{folder_id}' in parents and mimeType contains 'video/' and trashed=false",
            fields="files(id, name, createdTime)",
            orderBy="createdTime"
        ).execute()
        videos = results.get('files', [])
        print(f"[Drive] Trovati {len(videos)} video nella cartella {folder_id}")
        return videos
    except Exception as e:
        print(f"[Drive] Errore list_videos: {e}")
        return []


def download_video(file_id: str, dest_path: str) -> bool:
    try:
        service = get_drive_service()
        request = service.files().get_media(fileId=file_id)
        with open(dest_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        print(f"[Drive] Scaricato: {dest_path}")
        return True
    except Exception as e:
        print(f"[Drive] Errore download {file_id}: {e}")
        return False

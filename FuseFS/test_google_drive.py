import os
import io
import hashlib
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Authenticates and build the service
def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        'security.json', scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

# This function verifies MD5 checksum of a local file
def get_local_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Checks if file exists on Drive 
def find_file_on_drive(service, file_name, parent_id):
    query = f"'{parent_id}' in parents and name = '{file_name}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, md5Checksum)").execute()
    files = results.get('files', [])
    if files:
        return files[0]
    return None

def create_drive_folder(service, folder_name, parent_folder_id):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    print(f"Created folder {folder_name} (ID: {folder.get('id')})")
    return folder.get('id')

def upload_or_update_file(service, local_file_path, drive_folder_id):
    file_name = os.path.basename(local_file_path)
    local_md5 = get_local_file_md5(local_file_path)
    
    drive_file = find_file_on_drive(service, file_name, drive_folder_id)
    if drive_file:
        if drive_file.get('md5Checksum') == local_md5:
            print(f"Skipping {file_name}: No changes.")
            return
        else:
            # Updates existing file
            print(f"Updating {file_name}...")
            media = MediaFileUpload(local_file_path, resumable=True)
            updated_file = service.files().update(
                fileId=drive_file['id'],
                media_body=media
            ).execute()
            print(f"Updated {file_name} (ID: {updated_file.get('id')})")
    else:
        # Upload new file
        print(f"Uploading new file {file_name}...")
        media = MediaFileUpload(local_file_path, resumable=True)
        uploaded_file = service.files().create(
            body={'name': file_name, 'parents': [drive_folder_id]},
            media_body=media,
            fields='id'
        ).execute()
        print(f"Uploaded {file_name} (ID: {uploaded_file.get('id')})")

# Syncs folder recursively
def sync_folder(service, local_folder_path, drive_folder_id):
    folder_mapping = {local_folder_path: drive_folder_id}  # Maps local -> Drive folder IDs
    
    for root, dirs, files in os.walk(local_folder_path):
        drive_parent_id = folder_mapping[root]
        
        for d in dirs:
            local_subfolder_path = os.path.join(root, d)
            drive_subfolder_id = create_drive_folder(service, d, drive_parent_id)
            folder_mapping[local_subfolder_path] = drive_subfolder_id
        
        for f in files:
            local_file_path = os.path.join(root, f)
            upload_or_update_file(service, local_file_path, drive_parent_id)

# Service account credentials
service = get_drive_service()

local_folder_path = 'C:/Local path to synchronize to google drive'
drive_root_folder_id = 'Drive folder id'

sync_folder(service, local_folder_path, drive_root_folder_id)

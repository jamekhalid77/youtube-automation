# Google Drive se next video download karta hai upload ke liye
import os
import json
import io
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def download_next_video():
    """Download next video from Google Drive ready folder"""
    
    try:
        # Setup Google Drive API
        credentials_info = json.loads(os.environ['GDRIVE_CREDENTIALS'])
        credentials = Credentials.from_service_account_info(credentials_info)
        service = build('drive', 'v3', credentials=credentials)
        
        folder_id = os.environ['GDRIVE_FOLDER_ID']
        
        # Search for next video in ready_for_upload folder
        query = f"'{folder_id}' in parents and name contains 'video_' and mimeType contains 'video'"
        results = service.files().list(q=query, orderBy='name').execute()
        files = results.get('files', [])
        
        if not files:
            print("❌ No videos ready for upload")
            return False
        
        # Download first video
        video_file = files[0]
        file_id = video_file['id']
        filename = video_file['name']
        
        print(f"📥 Downloading: {filename}")
        
        request = service.files().get_media(fileId=file_id)
        file_content = io.BytesIO()
        downloader = MediaIoBaseDownload(file_content, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        # Save to local file
        with open(f"video_to_upload.mp4", 'wb') as f:
            f.write(file_content.getvalue())
        
        # Also download metadata if exists
        metadata_query = f"'{folder_id}' in parents and name = '{filename.replace('.mp4', '.info.json')}'"
        metadata_results = service.files().list(q=metadata_query).execute()
        metadata_files = metadata_results.get('files', [])
        
        if metadata_files:
            metadata_file = metadata_files[0]
            metadata_request = service.files().get_media(fileId=metadata_file['id'])
            metadata_content = io.BytesIO()
            metadata_downloader = MediaIoBaseDownload(metadata_content, metadata_request)
            
            done = False
            while done is False:
                status, done = metadata_downloader.next_chunk()
            
            with open("video_metadata.json", 'wb') as f:
                f.write(metadata_content.getvalue())
        
        print("✅ Video downloaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Download error: {e}")
        return False

if __name__ == "__main__":
    download_next_video()

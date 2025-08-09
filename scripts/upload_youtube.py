# YouTube pe video upload karta hai
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube():
    """Upload video to YouTube"""
    
    try:
        # Setup YouTube API
        token_info = json.loads(os.environ['YOUTUBE_TOKEN'])
        credentials = Credentials.from_authorized_user_info(token_info)
        
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Load video metadata
        metadata = {}
        if os.path.exists('video_metadata.json'):
            with open('video_metadata.json', 'r') as f:
                metadata = json.load(f)
        
        # Video details
        title = metadata.get('title', 'Automated Upload')[:100]
        description = metadata.get('description', '')[:4900] + "\n\n#shorts #viral"
        tags = metadata.get('tags', [])[:500]
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload video
        media = MediaFileUpload('video_to_upload.mp4', chunksize=-1, resumable=True)
        
        print(f"📤 Uploading: {title}")
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response['id']
        
        print(f"✅ Upload successful!")
        print(f"🔗 Video URL: https://youtube.com/watch?v={video_id}")
        
        # Update progress in Google Drive
        # (Mark this video as uploaded)
        
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

if __name__ == "__main__":
    upload_to_youtube()

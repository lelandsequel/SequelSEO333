"""
Google Drive Upload Module
Uploads sales reports and CSV files to Google Drive.
"""

import os
from pathlib import Path
from typing import Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


SCOPE = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def _get_drive_service():
    """Get Google Drive API service."""
    json_path = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_PATH", "./secrets/google-service-account.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Google credentials not found at: {json_path}")
    
    creds = Credentials.from_service_account_file(json_path, scopes=SCOPE)
    return build('drive', 'v3', credentials=creds)


def upload_file_to_drive(file_path: str, folder_id: Optional[str] = None) -> Optional[str]:
    """
    Upload a file to Google Drive.
    
    Args:
        file_path: Path to the file to upload
        folder_id: Optional Google Drive folder ID to upload to
        
    Returns:
        URL of the uploaded file, or None if upload failed
    """
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return None
    
    try:
        service = _get_drive_service()
        
        # Get folder ID from environment if not provided
        if folder_id is None:
            folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
        
        # Prepare file metadata
        file_name = Path(file_path).name
        file_metadata = {'name': file_name}
        
        # Add to folder if specified
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Determine MIME type
        if file_path.endswith('.csv'):
            mime_type = 'text/csv'
        elif file_path.endswith('.txt'):
            mime_type = 'text/plain'
        elif file_path.endswith('.pdf'):
            mime_type = 'application/pdf'
        else:
            mime_type = 'application/octet-stream'
        
        # Upload file
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        file_id = file.get('id')
        file_url = file.get('webViewLink')
        
        # Make file accessible (anyone with link can view)
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        print(f"✅ Uploaded to Google Drive: {file_name}")
        print(f"   URL: {file_url}")
        
        return file_url
        
    except FileNotFoundError as e:
        print(f"⚠️  Google credentials not found: {e}")
        print(f"   File saved locally only: {file_path}")
        return None
    except HttpError as e:
        print(f"⚠️  Google Drive API error: {e}")
        print(f"   File saved locally only: {file_path}")
        return None
    except Exception as e:
        print(f"⚠️  Failed to upload to Google Drive: {e}")
        print(f"   File saved locally only: {file_path}")
        return None


def upload_sales_report(report_path: str) -> Optional[str]:
    """
    Upload a sales report to Google Drive.
    Convenience wrapper for upload_file_to_drive.
    
    Args:
        report_path: Path to the sales report text file
        
    Returns:
        URL of the uploaded file, or None if upload failed
    """
    return upload_file_to_drive(report_path)


def upload_csv(csv_path: str) -> Optional[str]:
    """
    Upload a CSV file to Google Drive.
    Convenience wrapper for upload_file_to_drive.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        URL of the uploaded file, or None if upload failed
    """
    return upload_file_to_drive(csv_path)


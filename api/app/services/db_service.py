from supabase import create_client, Client
from api.app.core.config import settings
from api.app.models.schemas import ExtractedData
import json
import uuid

class DatabaseService:
    def __init__(self):
        self.client: Client = None
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            except Exception as e:
                print(f"⚠️ Failed to init Supabase: {e}")
        else:
            print("⚠️ SUPABASE_URL/KEY not found. DatabaseService running in MOCK mode.")

    def upload_file(self, file_contents: bytes, filename: str) -> str:
        """
        Uploads raw file to Supabase Storage bucket 'raw-bols'.
        Returns public URL or None.
        """
        if not self.client:
            return None
        
        try:
            # Generate unique path
            path = f"{uuid.uuid4()}_{filename}"
            res = self.client.storage.from_("raw-bols").upload(path, file_contents)
            
            # Get Public URL
            public_url = self.client.storage.from_("raw-bols").get_public_url(path)
            return public_url
        except Exception as e:
            print(f"❌ Storage Upload Failed: {e}")
            return None

    def save_document(self, filename: str, url: str, data: ExtractedData) -> str:
        """
        Saves metadata and extracted JSON to 'documents' table.
        """
        if not self.client:
            return None
            
        try:
            payload = {
                "filename": filename,
                "url": url,
                "status": "processed",
                "extracted_data": json.loads(data.json()), # Store full JSON
                "confidence_score": data.confidence_score
            }
            
            data = self.client.table("documents").insert(payload).execute()
            if data.data:
                return data.data[0]['id']
            return None
        except Exception as e:
            print(f"❌ DB Save Failed: {e}")
            return None

db_service = DatabaseService()

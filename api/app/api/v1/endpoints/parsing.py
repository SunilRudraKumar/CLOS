from fastapi import APIRouter, UploadFile, File, HTTPException
from api.app.services.ocr_service import ocr_service
from api.app.models.schemas import ExtractedData

router = APIRouter()

@router.post("/parse", response_model=ExtractedData)
async def parse_document(file: UploadFile = File(...)):
    """
    Upload a Bill of Lading (PDF/Image) for parsing.
    
    Process:
    1. Reads file into memory (limit size in prod!)
    2. Runs OCR + LLM extraction
    3. Validates checksums and codes
    4. Returns structured JSON
    """
    if not file.filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
         raise HTTPException(status_code=400, detail="Invalid file type. Only PDF/Image allowed.")
    
    try:
        contents = await file.read()
        
        # Call the service
        result = ocr_service.process_document(contents, file.filename)
        
        # 3. Persist (Phase 5)
        try:
            from api.app.services.db_service import db_service
            # Upload File
            public_url = db_service.upload_file(contents, file.filename)
            if public_url:
                # Save Record
                doc_id = db_service.save_document(file.filename, public_url, result)
                result.id = doc_id # Pass back the ID
        except Exception as e:
            print(f"⚠️ Persistence Warning: {e}")
            # Non-blocking failure. If DB fails, we still return the extracted data.

        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")

@router.post("/export", response_model=str)
async def export_xml(data: ExtractedData):
    """
    Converts validated JSON data into 'UniversalShipment.xml' format.
    """
    try:
        from api.app.services.xml_service import xml_service
        xml_content = xml_service.generate_universal_shipment(data)
        return xml_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

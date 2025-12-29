from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Shared Models ---

class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class LayoutLine(BaseModel):
    text: str
    bbox: BoundingBox
    polygon: Optional[List[List[float]]] = None

class Container(BaseModel):
    id: Optional[str] = None
    container_number: str = Field(..., description="The shipping container ID (e.g. MSKU1234567)")
    seal_number: Optional[str] = None
    package_count: Optional[int] = None
    weight_gross: Optional[float] = None
    weight_unit: str = "KG"
    volume_cbm: Optional[float] = None
    description: Optional[str] = None
    
    # Validation Flags (populated by backend)
    is_valid_checksum: bool = True
    validation_message: Optional[str] = None

class ShipmentHeader(BaseModel):
    shipper: Optional[str] = None
    consignee: Optional[str] = None
    notify_party: Optional[str] = None
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    pol_locode: Optional[str] = None # Validated LOCODE
    pod_locode: Optional[str] = None # Validated LOCODE
    hbl_number: Optional[str] = None
    mbl_number: Optional[str] = None
    scac_code: Optional[str] = None

# --- API Request/Response Schemas ---

class ExtractedData(BaseModel):
    """
    The main payload returned after OCR + LLM extraction.
    """
    header: ShipmentHeader
    containers: List[Container] = []
    
    # Metadata
    confidence_score: float = 0.0
    processing_time_ms: int = 0
    confidence_score: float = 0.0
    processing_time_ms: int = 0
    raw_text: Optional[str] = None
    layout: Optional[List[LayoutLine]] = None

class ProcessingStatusResponse(BaseModel):
    task_id: str
    status: str # "PENDING", "PROCESSING", "COMPLETED", "FAILED"
    result: Optional[ExtractedData] = None
    error: Optional[str] = None

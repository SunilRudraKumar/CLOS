export interface BoundingBox {
    x: number;
    y: number;
    width: number;
    height: number;
}

export interface LayoutLine {
    text: string;
    bbox: BoundingBox;
}

export interface Container {
    id?: string;
    container_number: string;
    seal_number?: string;
    package_count?: number;
    weight_gross?: number;
    weight_unit: string;
    volume_cbm?: number;
    description?: string;
    is_valid_checksum: boolean;
    validation_message?: string;
}

export interface ShipmentHeader {
    shipper?: string;
    consignee?: string;
    notify_party?: string;
    vessel_name?: string;
    voyage_number?: string;
    port_of_loading?: string;
    port_of_discharge?: string;
    pol_locode?: string;
    pod_locode?: string;
    hbl_number?: string;
    mbl_number?: string;
    scac_code?: string;
}

export interface ExtractedData {
    header: ShipmentHeader;
    containers: Container[];
    confidence_score: number;
    processing_time_ms: number;
    raw_text?: string;
    layout?: LayoutLine[];
}

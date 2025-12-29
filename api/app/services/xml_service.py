import xml.etree.ElementTree as ET
from xml.dom import minidom
from api.app.models.schemas import ExtractedData

class XmlService:
    """
    Generates 'UniversalShipment.xml' for CargoWise integration.
    """
    
    @staticmethod
    def generate_universal_shipment(data: ExtractedData) -> str:
        """
        Maps ExtractedData -> CargoWise XML format.
        """
        # Root Element
        root = ET.Element("UniversalShipment", xmlns="http://www.cargowise.com/Schemas/Universal/2011/11")
        
        # Shipment Element
        shipment = ET.SubElement(root, "Shipment")
        
        # --- 1. Header Mapping ---
        # DataContext
        data_context = ET.SubElement(shipment, "DataContext")
        ET.SubElement(data_context, "DataSourceCollection").text = "CLOS_OCR"
        
        # Transport Leg (Vessel/Voyage/Pol/Pod)
        # Note: CargoWise XML structure is complex; this is a simplified 'flat' mapping for MVP.
        # Making assumptions on where fields go based on standard UniversalShipment usage.
        
        # TransportLegCollection -> TransportLeg -> VoyageNumber, VesselName
        # LocalProcessing (Header Fields)
        local_processing = ET.SubElement(shipment, "LocalProcessing")
        
        # OrganizationAddressCollection
        org_collection = ET.SubElement(shipment, "OrganizationAddressCollection")
        
        # Shipper (Consignor)
        if data.header.shipper:
            shipper = ET.SubElement(org_collection, "OrganizationAddress")
            ET.SubElement(shipper, "AddressType").text = "Consignor"
            ET.SubElement(shipper, "CompanyName").text = data.header.shipper

        # Consignee (Consignee)
        if data.header.consignee:
            consignee = ET.SubElement(org_collection, "OrganizationAddress")
            ET.SubElement(consignee, "AddressType").text = "Consignee"
            ET.SubElement(consignee, "CompanyName").text = data.header.consignee

        # --- 2. Container Mapping ---
        container_collection = ET.SubElement(shipment, "ContainerCollection")
        
        for c in data.containers:
            if not c.is_valid_checksum:
                # OPTIONAL: Skip invalid containers or flag them? 
                # For "Firewall" logic, we usually export them but maybe add a Note?
                # For MVP, we export all but maybe prefix description with [INVALID CHECKSUM]
                pass
                
            container_xml = ET.SubElement(container_collection, "Container")
            ET.SubElement(container_xml, "ContainerNumber").text = c.container_number
            
            if c.seal_number:
                ET.SubElement(container_xml, "SealNumber").text = c.seal_number
            
            if c.description:
                desc = c.description
                if not c.is_valid_checksum:
                    desc = f"[INVALID ISO6346] {desc}"
                ET.SubElement(container_xml, "GoodsDescription").text = desc

        # Pretty Print
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        return xml_str

xml_service = XmlService()

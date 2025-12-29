import re
from typing import Optional, List
from stdnum import iso6346 # type: ignore

class Validator:
    """
    The Logistics Firewall Validator.
    Ensures all incoming data meets strict international standards before downstream processing.
    """

    @staticmethod
    def validate_container_iso6346(container_number: str) -> bool:
        """
        Validates a shipping container number using the ISO 6346 standard checksum.
        
        Args:
            container_number (str): The container number to validate (e.g., "MSKU1234567")
            
        Returns:
            bool: True if valid, False otherwise.
        """
        if not container_number:
            return False
        
        # Clean input: remove spaces, dashes, turn to uppercase
        clean_number = re.sub(r'[^A-Z0-9]', '', container_number.upper())
        
        try:
            iso6346.validate(clean_number)
            return True
        except Exception:
            # stdnum validation failed or raised an exception (e.g. format error)
            return False

    @staticmethod
    def validate_scac(scac_code: str, known_scacs: Optional[List[str]] = None) -> bool:
        """
        Validates a Standard Carrier Alpha Code (SCAC).
        Format: 2-4 letters.
        
        Args:
            scac_code (str): The SCAC code to validate (e.g., "MAEU")
            known_scacs (list): Optional list of valid SCACs to check against.
            
        Returns:
            bool: True if valid format (and exists in known_list if provided).
        """
        if not scac_code:
            return False
            
        code = scac_code.upper().strip()
        
        # Basic Format Check: 2-4 alphabetic characters
        if not re.match(r'^[A-Z]{2,4}$', code):
            return False
            
        # If we have a database/master list of SCACs, check against it
        if known_scacs and code not in known_scacs:
            return False
            
        return True

    @staticmethod
    def validate_locode(locode: str, known_locodes: Optional[List[str]] = None) -> bool:
        """
        Validates a UN/LOCODE (United Nations Code for Trade and Transport Locations).
        Format: 5 characters (2 letters for country + 3 alphanumeric for location).
        
        Args:
            locode (str): The LOCODE to validate (e.g., "CNSHA", "USNYC")
            known_locodes (list): Optional list of valid LOCODEs to check against.
            
        Returns:
            bool: True if valid format.
        """
        if not locode:
            return False
            
        code = locode.upper().strip()
        
        # Format: 2 letters (Classic ISO 3166-1 alpha-2 country code) + 3 alphanumeric
        # Valid: USNYC, CNHGH, NLRTM
        if not re.match(r'^[A-Z]{2}[A-Z0-9]{3}$', code):
            return False
            
        if known_locodes and code not in known_locodes:
            return False
            
        return True

# Singleton instance for easy import
validator = Validator()

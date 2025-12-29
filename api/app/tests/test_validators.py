from api.app.core.validators import validator

def test_iso6346_validation():
    print("Testing ISO 6346 Container Validation...")
    
    # Valid Cases
    assert validator.validate_container_iso6346("MSKU1234565") == True
    assert validator.validate_container_iso6346("MSKU 1234565") == True # Should handle spaces
    assert validator.validate_container_iso6346("msku1234565") == True # Should handle lowercase
    
    # Invalid Cases
    assert validator.validate_container_iso6346("MSKU1234568") == False # Bad checksum
    assert validator.validate_container_iso6346("ABC") == False # Too short
    assert validator.validate_container_iso6346("MSKU123456") == False # Missing digit
    
    print("✅ ISO 6346 Tests Passed")

def test_scac_validation():
    print("\nTesting SCAC Validation...")
    
    # Valid Format
    assert validator.validate_scac("MAEU") == True
    assert validator.validate_scac("XY") == True
    
    # Invalid Format
    assert validator.validate_scac("A") == False # Too short
    assert validator.validate_scac("ABCDE") == False # Too long
    assert validator.validate_scac("1234") == False # Numbers not allowed
    
    # Check against known list
    valid_list = ["MAEU", "COSU", "MSCU"]
    assert validator.validate_scac("MAEU", known_scacs=valid_list) == True
    assert validator.validate_scac("OOLU", known_scacs=valid_list) == False # Format valid, but not in list
    
    print("✅ SCAC Tests Passed")

def test_locode_validation():
    print("\nTesting UN/LOCODE Validation...")
    
    # Valid Format
    assert validator.validate_locode("USNYC") == True # New York
    assert validator.validate_locode("CNSHA") == True # Shanghai
    
    # Invalid Format
    assert validator.validate_locode("US NYC") == False # No spaces allowed in strict check (caller should clean)
    assert validator.validate_locode("US") == False # Too short
    assert validator.validate_locode("USNYC1") == False # Too long
    assert validator.validate_locode("12ABC") == False # Country code must be letters
    
    print("✅ LOCODE Tests Passed")

if __name__ == "__main__":
    try:
        test_iso6346_validation()
        test_scac_validation()
        test_locode_validation()
        print("\n🎉 ALL TESTS PASSED!")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

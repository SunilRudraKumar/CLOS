from fastapi.testclient import TestClient
from api.app.main import app
import json

client = TestClient(app)

def test_parse_endpoint():
    print("🚀 Starting API Integration Test...")
    
    # 1. Simulate File Upload
    # We create a dummy PDF in memory
    files = {
        'file': ('test_bol.pdf', b'%PDF-1.4 ... dummy content', 'application/pdf')
    }
    
    print("📤 Sending POST request to /api/v1/parsing/parse...")
    response = client.post("/api/v1/parsing/parse", files=files)
    
    # 2. Check HTTP Status
    if response.status_code != 200:
        print(f"❌ Failed: Status Code {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print("✅ Request Successful. received JSON response.")
    
    # 3. Inspect Payload
    containers = data.get("containers", [])
    print(f"📦 Found {len(containers)} containers in response.")
    
    # 4. Verify Validation Logic (The "Mock" data has 1 valid, 1 invalid)
    
    # 4a. Check Valid Container
    valid_c = next((c for c in containers if c["container_number"] == "MSKU1234565"), None)
    if valid_c and valid_c["is_valid_checksum"]:
        print("✅ Correctly identified VALID container: MSKU1234565")
    else:
        print("❌ Failed to identify VALID container or it wasn't valid.")

    # 4b. Check Invalid Container (The "Firewall" test)
    invalid_c = next((c for c in containers if c["container_number"] == "MSKU1234568"), None)
    if invalid_c:
        if not invalid_c["is_valid_checksum"] and "Invalid ISO 6346 checksum" in invalid_c["validation_message"]:
            print(f"✅ Correctly BLOCKED invalid container: MSKU1234568")
            print(f"   Reason: {invalid_c['validation_message']}")
        else:
            print("❌ 'Firewall' Logic Failed! Invalid container was marked as valid.")
    else:
        print("❌ Could not find expected test container MSKU1234568.")

if __name__ == "__main__":
    test_parse_endpoint()

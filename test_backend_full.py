
import os
import requests
import time
from reportlab.pdfgen import canvas

PDF_FILE = "test_sample.pdf"
API_URL = "http://localhost:8001/api/v1/parsing/parse"

def create_pdf():
    print(f"📄 Generating {PDF_FILE}...")
    c = canvas.Canvas(PDF_FILE)
    c.drawString(100, 750, "BILL OF LADING")
    c.drawString(100, 730, "Shipper: ACME Corp")
    c.drawString(100, 715, "123 Industrial Way, CA")
    
    c.drawString(100, 680, "Consignee: Global Tech Ltd")
    c.drawString(100, 665, "456 Tech Park, NY")
    
    c.drawString(100, 630, "Container: MSKU1234567")
    c.drawString(100, 615, "Seal: 999888")
    c.drawString(100, 600, "Description: Electronics Parts")
    
    c.save()
    print("✅ PDF Created.")

def test_api():
    if not os.path.exists(PDF_FILE):
        create_pdf()
        
    print(f"🚀 Sending request to {API_URL}...")
    start = time.time()
    
    try:
        with open(PDF_FILE, 'rb') as f:
            files = {'file': (PDF_FILE, f, 'application/pdf')}
            response = requests.post(API_URL, files=files)
            
        elapsed = time.time() - start
        print(f"⏱️ Time taken: {elapsed:.2f}s")
        
        if response.status_code == 200:
            print("✅ Status: 200 OK")
            data = response.json()
            
            layout = data.get("layout", [])
            print(f"📦 Layout Lines: {len(layout)}")
            if len(layout) > 0:
                print("   [First Line]:", layout[0])
            else:
                print("⚠️ NO LAYOUT DETECTED!")
                
            header = data.get("header", {})
            print("📝 Header:", header)
            
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_api()

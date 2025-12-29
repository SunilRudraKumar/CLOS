
try:
    print("Attempting to import surya.ocr...")
    from surya.ocr import run_ocr
    print("Success!")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Other Error: {e}")

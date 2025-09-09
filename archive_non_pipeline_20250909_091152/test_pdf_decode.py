#!/usr/bin/env python3
"""
Test script to debug PDF base64 decoding
"""

import base64
import os

def test_pdf_decode():
    """Test PDF base64 decoding."""
    
    # Test the base64 data from our test case
    test_base64 = "JVBERi0xLjMNCiXH7I+iDQoxIDAgb2JqDQo8PA0KICAvQ3JlYXRvciAoUG9seWNhbSkNCiAgL1Byb2R1Y2VyIChQb2x5Y2FtKQ0KICAvVGl0bGUgKFNwYXRpYWxSZXBvcnQpDQogIC9TdWJqZWN0IChGbG9vcnBsYW4pDQogIC9DcmVhdGlvbkRhdGUgKEQ6MjAyNTA1MjgxMDU1MjBaKQ0KPj4NCmVuZG9iag0KMiAwIG9iag0KPDwNCiAgL1R5cGUgL1BhZ2VzDQogIC9LaWRzIFsgNiAwIFIgMTYwNiAwIFIgMzIyMSAwIFIgMzU3MSAwIFIgNDU4NiAwIFIgNTU1OSAwIFIgNjUyNSAwIFIgODMxMiAwIFIgODYzNiAwIFIgOTg5NiAwIFIgMTAxODIgMCBSIDExMjA2IDAgUiAxMTQ4NCAwIFIgMTE4MzUgMCBSIF0NCiAgL0NvdW50IDE0DQo+Pg0KZW5kb2JqDQozIDAgb2JqDQo8PA0KICAvVHlwZSAvQ2F0YWxvZw0KICAvUGFnZXMgMiAwIFINCj4+DQplbmRvYmoNCjQgMCBvYmoNCjw8DQogIC9UeXBlIC9Gb250DQogIC9TdWJ0eXBlIC9UeXBlMQ0KICAvQmFzZUZvbnQgL1RpbWVzLVJvbWFuDQogIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nDQo+Pg0KZW5kb2JqDQo1IDAgb2JqDQo8PA0KICAvVHlwZSAvRm9udA0KICAvU3VidHlwZSAvVHlwZTENCiAgL0Jhc2VGb250IC9IZWx2ZXRpY2ENCiAgL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcNCj4+DQplbmRvYmoNCjYgMCBvYmoNCjw8DQogIC9UeXBlIC9QYWdlDQogIC9QYXJlbnQgMiAwIFINCiAgL01lZGlhQm94IFswIDAgNzkyLjAwMDAwMCA2MTIuMDAwMDAwXQ0KICAvUmVzb3Vy"
    
    print("🧪 Testing PDF base64 decoding...")
    print("=" * 50)
    
    try:
        # Decode base64 to bytes
        pdf_bytes = base64.b64decode(test_base64)
        print(f"✅ Base64 decoded successfully")
        print(f"📊 Decoded size: {len(pdf_bytes)} bytes")
        print(f"🔍 First 100 bytes: {pdf_bytes[:100]}")
        
        # Check if it starts with PDF header
        if pdf_bytes.startswith(b'%PDF'):
            print("✅ PDF header detected correctly")
        else:
            print("❌ PDF header not found")
            print(f"🔍 Actual start: {pdf_bytes[:20]}")
        
        # Write to test file
        test_file = "test_decoded.pdf"
        with open(test_file, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ Wrote test file: {test_file}")
        
        # Check file type
        import subprocess
        result = subprocess.run(['file', test_file], capture_output=True, text=True)
        print(f"📁 File type: {result.stdout.strip()}")
        
        # Check file size
        file_size = os.path.getsize(test_file)
        print(f"📊 File size: {file_size} bytes")
        
        # Clean up
        os.remove(test_file)
        print("🧹 Cleaned up test file")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_pdf_decode()


#!/usr/bin/env python3
"""
Test script to check if base64 data is being corrupted
"""

import base64
import os
import tempfile

def test_base64_integrity():
    """Test if base64 data maintains integrity through the process."""
    
    print("🧪 Testing Base64 Data Integrity...")
    print("=" * 50)
    
    # Test with a real PDF file
    test_pdf = "Transcript1.pdf"
    if not os.path.exists(test_pdf):
        print(f"❌ Test PDF not found: {test_pdf}")
        return
    
    print(f"📁 Testing with: {test_pdf}")
    original_size = os.path.getsize(test_pdf)
    print(f"📊 Original file size: {original_size} bytes")
    
    try:
        # Step 1: Read and encode the PDF
        print("\n🔍 Step 1: Reading and encoding PDF...")
        with open(test_pdf, 'rb') as f:
            pdf_bytes = f.read()
        
        print(f"✅ Read {len(pdf_bytes)} bytes from PDF")
        
        # Check PDF header
        if pdf_bytes.startswith(b'%PDF'):
            print("✅ PDF header detected: %PDF")
        else:
            print("❌ PDF header not found")
            print(f"🔍 Actual start: {pdf_bytes[:20]}")
        
        # Step 2: Encode to base64
        print("\n🔍 Step 2: Encoding to base64...")
        base64_string = base64.b64encode(pdf_bytes).decode('utf-8')
        print(f"✅ Encoded to base64: {len(base64_string)} characters")
        
        # Step 3: Decode back to bytes (simulating what the API does)
        print("\n🔍 Step 3: Decoding base64 back to bytes...")
        decoded_bytes = base64.b64decode(base64_string.encode('utf-8'))
        print(f"✅ Decoded back to: {len(decoded_bytes)} bytes")
        
        # Step 4: Check if the decoded data is identical
        print("\n🔍 Step 4: Checking data integrity...")
        if pdf_bytes == decoded_bytes:
            print("✅ Data integrity maintained - decoded bytes match original")
        else:
            print("❌ Data corruption detected!")
            print(f"🔍 Original size: {len(pdf_bytes)} bytes")
            print(f"🔍 Decoded size: {len(decoded_bytes)} bytes")
            
            # Check first and last bytes
            if len(decoded_bytes) > 0:
                print(f"🔍 Original first 20 bytes: {pdf_bytes[:20]}")
                print(f"🔍 Decoded first 20 bytes: {decoded_bytes[:20]}")
                print(f"🔍 Original last 20 bytes: {pdf_bytes[-20:]}")
                print(f"🔍 Decoded last 20 bytes: {decoded_bytes[-20:]}")
        
        # Step 5: Write decoded file and check
        print("\n🔍 Step 5: Writing decoded file...")
        temp_dir = tempfile.mkdtemp(prefix='test_pdf_')
        decoded_file = os.path.join(temp_dir, 'decoded.pdf')
        
        with open(decoded_file, 'wb') as f:
            f.write(decoded_bytes)
        
        decoded_file_size = os.path.getsize(decoded_file)
        print(f"✅ Wrote decoded file: {decoded_file}")
        print(f"📊 Decoded file size: {decoded_file_size} bytes")
        
        # Check file type
        import subprocess
        result = subprocess.run(['file', decoded_file], capture_output=True, text=True)
        print(f"📁 Decoded file type: {result.stdout.strip()}")
        
        # Check if it's still a valid PDF
        with open(decoded_file, 'rb') as f:
            first_bytes = f.read(50)
        if first_bytes.startswith(b'%PDF'):
            print("✅ Decoded file still has PDF header")
        else:
            print("❌ Decoded file lost PDF header")
            print(f"🔍 Actual start: {first_bytes[:20]}")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up temp directory: {temp_dir}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 50)

if __name__ == "__main__":
    test_base64_integrity()


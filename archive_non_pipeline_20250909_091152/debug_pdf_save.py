#!/usr/bin/env python3
"""
Debug script to test PDF saving process
"""

import base64
import os
import tempfile

def test_pdf_save():
    """Test the exact PDF saving process used by the API."""
    
    print("🧪 Debugging PDF Save Process...")
    print("=" * 50)
    
    # Test with a small valid PDF base64
    test_base64 = "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFs2IDAgUiAxNjA2IDAgUiAzMjIxIDAgUiAzNTcxIDAgUiA0NTg2IDAgUiA1NTU5IDAgUiA2NTI1IDAgUiA4MzEyIDAgUiA4NjM2IDAgUiA5ODk2IDAgUiAxMDE4MiAwIFIgMTEyMDYgMCBSIDExNDg0IDAgUiAxMTgzNSAwIFJdCi9Db3VudCAxNAo+PgplbmRvYmoKMyAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjQgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvVGltZXMtUm9tYW5lCi9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nCj4+CmVuZG9iago1IDAgb2JqCj4+CmVuZG9iag=="
    
    print(f"📊 Base64 length: {len(test_base64)} characters")
    
    try:
        # Step 1: Decode base64 to bytes (exactly like the API does)
        print("\n🔍 Step 1: Base64 decoding...")
        pdf_bytes = base64.b64decode(test_base64.encode('utf-8'))
        print(f"✅ Decoded size: {len(pdf_bytes)} bytes")
        print(f"🔍 First 50 bytes: {pdf_bytes[:50]}")
        
        # Check PDF header
        if pdf_bytes.startswith(b'%PDF'):
            print("✅ PDF header detected: %PDF")
        else:
            print("❌ PDF header not found")
            print(f"🔍 Actual start: {pdf_bytes[:20]}")
        
        # Step 2: Create temp directory (like the API does)
        print("\n🔍 Step 2: Creating temp directory...")
        temp_dir = tempfile.mkdtemp(prefix='test_pdf_')
        polycam_path = os.path.join(temp_dir, 'polycam.pdf')
        print(f"📁 Temp directory: {temp_dir}")
        print(f"📁 PDF path: {polycam_path}")
        
        # Step 3: Write file in binary mode (exactly like the API does)
        print("\n🔍 Step 3: Writing PDF file...")
        with open(polycam_path, 'wb') as f:
            f.write(pdf_bytes)
        print(f"✅ File written: {polycam_path}")
        
        # Step 4: Check the saved file
        print("\n🔍 Step 4: Checking saved file...")
        if os.path.exists(polycam_path):
            file_size = os.path.getsize(polycam_path)
            print(f"📊 File size: {file_size} bytes")
            
            # Check file type
            import subprocess
            result = subprocess.run(['file', polycam_path], capture_output=True, text=True)
            print(f"📁 File type: {result.stdout.strip()}")
            
            # Try to read first few bytes
            with open(polycam_path, 'rb') as f:
                first_bytes = f.read(50)
            print(f"🔍 First 50 bytes of saved file: {first_bytes}")
            
            # Check if it's still a valid PDF
            if first_bytes.startswith(b'%PDF'):
                print("✅ Saved file still has PDF header")
            else:
                print("❌ Saved file lost PDF header")
        else:
            print("❌ File was not created")
        
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
    test_pdf_save()


#!/usr/bin/env python3
"""
Test script for large transcript processing
"""
import os
import json
import time
from process_transcript import process_transcript

def test_large_transcript():
    """Test processing of large transcript files"""
    
    # Test with the large JSON file
    input_file = "/Users/bhakt/Downloads/20250812173901.json"
    output_dir = "test_large_output"
    
    if not os.path.exists(input_file):
        print(f"❌ Test file not found: {input_file}")
        return
    
    print(f"🧪 Testing large transcript processing...")
    print(f"📁 Input: {input_file}")
    print(f"📁 Output: {output_dir}")
    
    # Get file size
    file_size = os.path.getsize(input_file)
    print(f"📊 File size: {file_size/1024:.1f}KB")
    
    # Process the transcript
    start_time = time.time()
    success = process_transcript(input_file, output_dir, max_tokens=2000)
    processing_time = time.time() - start_time
    
    if success:
        print(f"✅ Processing completed in {processing_time:.2f} seconds")
        
        # Check output
        if os.path.exists(output_dir):
            chunks = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
            print(f"📝 Created {len(chunks)} chunks:")
            
            total_chars = 0
            for chunk_file in sorted(chunks):
                chunk_path = os.path.join(output_dir, chunk_file)
                with open(chunk_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_chars += len(content)
                    print(f"   - {chunk_file}: {len(content)} characters")
            
            print(f"📊 Total characters processed: {total_chars:,}")
            print(f"📊 Compression ratio: {file_size/total_chars:.2f}x")
        else:
            print("❌ Output directory not created")
    else:
        print("❌ Processing failed")
    
    # Cleanup
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
        print("🧹 Cleaned up test output")

if __name__ == "__main__":
    test_large_transcript()


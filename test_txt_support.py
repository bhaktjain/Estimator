#!/usr/bin/env python3
"""
Test script to verify .txt transcript support
"""
import os
import tempfile
import shutil
from pathlib import Path

def test_process_transcript():
    """Test that process_transcript.py handles .txt files"""
    print("Testing process_transcript.py with .txt file...")
    
    # Create a test transcript
    test_content = """
    Speaker 1: We need to renovate the kitchen.
    Speaker 2: I recommend new cabinets and countertops.
    Speaker 1: What about the flooring?
    Speaker 2: Luxury vinyl plank would work well. The kitchen is about 200 square feet.
    """
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test transcript file
        transcript_path = os.path.join(temp_dir, 'test_transcript.txt')
        with open(transcript_path, 'w') as f:
            f.write(test_content)
        
        # Create output directory
        output_dir = os.path.join(temp_dir, 'chunks')
        
        # Run process_transcript
        import subprocess
        result = subprocess.run(
            ['python3', 'process_transcript.py', transcript_path, '--output_dir', output_dir, '--max_tokens', '500'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ FAILED: {result.stderr}")
            return False
        
        # Check that chunks were created
        chunk_files = list(Path(output_dir).glob('*.txt'))
        if not chunk_files:
            print("❌ FAILED: No chunks created")
            return False
        
        print(f"✅ SUCCESS: Created {len(chunk_files)} chunk(s)")
        
        # Verify chunk content
        with open(chunk_files[0], 'r') as f:
            chunk_content = f.read()
            if 'kitchen' in chunk_content.lower():
                print("✅ SUCCESS: Chunk content verified")
                return True
            else:
                print("❌ FAILED: Chunk content incorrect")
                return False

def test_api_txt_support():
    """Test that API accepts .txt files"""
    print("\nTesting API .txt file support...")
    
    # Check that ALLOWED_EXTENSIONS includes 'txt'
    import sys
    sys.path.insert(0, 'archive_non_pipeline_20250909_091152')
    
    try:
        from app_fastapi import ALLOWED_EXTENSIONS
        
        if 'txt' in ALLOWED_EXTENSIONS:
            print(f"✅ SUCCESS: API allows .txt files (extensions: {ALLOWED_EXTENSIONS})")
            return True
        else:
            print(f"❌ FAILED: API does not allow .txt files (extensions: {ALLOWED_EXTENSIONS})")
            return False
    except Exception as e:
        print(f"❌ FAILED: Could not import API: {e}")
        return False

def main():
    print("=" * 60)
    print("Testing .txt Transcript Support")
    print("=" * 60)
    
    results = []
    
    # Test 1: process_transcript.py
    results.append(("process_transcript.py", test_process_transcript()))
    
    # Test 2: API support
    results.append(("API .txt support", test_api_txt_support()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! The system is ready to accept .txt transcripts.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())

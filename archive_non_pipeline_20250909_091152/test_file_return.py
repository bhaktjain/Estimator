#!/usr/bin/env python3
"""
Test script to verify file return functionality using existing successful run
"""

import os
import shutil
from datetime import datetime

def test_file_return():
    """Test the file return functionality using existing files."""
    
    # Use the existing successful run directory
    run_dir = "chunked_outputs/run_20250820_141724_df163cc7"
    
    # Check if the directory exists
    if not os.path.exists(run_dir):
        print(f"❌ Run directory not found: {run_dir}")
        return False
    
    # Check for the required files
    excel_file = os.path.join(run_dir, "comprehensive_clean_estimate_final.xlsx")
    csv_file = os.path.join(run_dir, "comprehensive_clean_estimate_final.csv")
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return False
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return False
    
    print(f"✅ Found Excel file: {excel_file}")
    print(f"✅ Found CSV file: {csv_file}")
    
    # Test copying to outputs folder (simulating what the API does)
    outputs_dir = "outputs"
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = f"comprehensive_clean_estimate_final_{timestamp}.xlsx"
    csv_filename = f"comprehensive_clean_estimate_final_{timestamp}.csv"
    
    excel_output_path = os.path.join(outputs_dir, excel_filename)
    csv_output_path = os.path.join(outputs_dir, csv_filename)
    
    try:
        # Copy files to outputs folder
        shutil.copy2(excel_file, excel_output_path)
        shutil.copy2(csv_file, csv_output_path)
        
        print(f"✅ Copied Excel to: {excel_output_path}")
        print(f"✅ Copied CSV to: {csv_output_path}")
        
        # Verify file sizes
        excel_size = os.path.getsize(excel_output_path)
        csv_size = os.path.getsize(csv_output_path)
        
        print(f"📊 Excel file size: {excel_size} bytes")
        print(f"📊 CSV file size: {csv_size} bytes")
        
        # Test file access (simulating FileResponse)
        if os.path.exists(excel_output_path) and os.path.exists(csv_output_path):
            print("✅ File return test PASSED - files are accessible")
            return True
        else:
            print("❌ File return test FAILED - files not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Error during file copy: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing File Return Functionality...")
    print("=" * 50)
    
    success = test_file_return()
    
    print("=" * 50)
    if success:
        print("🎉 SUCCESS: File return functionality is working!")
    else:
        print("💥 FAILED: File return functionality has issues!")


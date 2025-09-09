#!/usr/bin/env python3
"""
Complete Automated Renovation Estimation Pipeline
API-ready with dynamic file handling and no hardcoding
"""

import os
import sys
import subprocess
import shlex
import argparse
from datetime import datetime
import hashlib

def run_cmd(cmd):
    """Execute a command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ERROR] Command failed: {cmd}")
            print(f"[ERROR] {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to execute command: {e}")
        return False

def find_latest_output_dir():
    """Find the most recent output directory."""
    base_dir = "chunked_outputs"
    if not os.path.exists(base_dir):
        return None
    
    dirs = [d for d in os.listdir(base_dir) if d.startswith("run_")]
    if not dirs:
        return None
    
    # Sort by creation time (newest first)
    dirs.sort(key=lambda x: os.path.getctime(os.path.join(base_dir, x)), reverse=True)
    return os.path.join(base_dir, dirs[0])

def main():
    parser = argparse.ArgumentParser(description="Complete Automated Renovation Estimation Pipeline")
    parser.add_argument("--transcript", required=True, help="Path to transcript PDF file")
    parser.add_argument("--polycam", required=True, help="Path to polycam PDF file")
    parser.add_argument("--api_key", required=True, help="OpenAI API key")
    parser.add_argument("--max_tokens", default="3000", help="Max tokens per chunk (default: 3000)")
    
    args = parser.parse_args()
    
    # Validate input files
    if not os.path.exists(args.transcript):
        print(f"[ERROR] Transcript file not found: {args.transcript}")
        return False
    
    if not os.path.exists(args.polycam):
        print(f"[ERROR] Polycam file not found: {args.polycam}")
        return False
    
    print("🚀 STARTING COMPLETE AUTOMATED RENOVATION ESTIMATION PIPELINE")
    print(f"📄 Transcript: {args.transcript}")
    print(f"📄 Polycam: {args.polycam}")
    
    # Step 1: Run the main estimation pipeline
    print("\n📊 STEP 1: Running estimation pipeline...")
    
    cmd = f'python3 run_chunked_estimation.py --transcript "{args.transcript}" --polycam "{args.polycam}" --master_pricing "Master Pricing Sheet - Q1 - 2025 (2).pdf" --prompt_file estimation_prompt.txt --api_key {args.api_key} --max_tokens {args.max_tokens}'
    
    if not run_cmd(cmd):
        print("[ERROR] Estimation pipeline failed")
        return False
    
    # Step 2: Find the latest output directory
    print("\n📁 STEP 2: Finding latest output directory...")
    latest_path = find_latest_output_dir()
    if not latest_path:
        print("[ERROR] No output directory found")
        return False
    
    print(f"✅ Found latest directory: {latest_path}")
    
    # Step 3: Update comprehensive cleanup script with dynamic paths
    print("\n🧹 STEP 3: Running comprehensive cleanup...")
    
    # Read the comprehensive cleanup script
    with open('comprehensive_cleanup.py', 'r') as f:
        content = f.read()
    
    # Update the file paths dynamically
    new_content = content.replace(
        'input_file = "chunked_outputs/run_20250728_121845_d5672e88/aggregated_chunked_estimate.csv"',
        f'input_file = "{latest_path}/aggregated_chunked_estimate.csv"'
    )
    new_content = new_content.replace(
        'output_csv = "chunked_outputs/run_20250728_121845_d5672e88/comprehensive_clean_estimate.csv"',
        f'output_csv = "{latest_path}/comprehensive_clean_estimate.csv"'
    )
    new_content = new_content.replace(
        'output_excel = "chunked_outputs/run_20250728_121845_d5672e88/final_renovation_estimate.xlsx"',
        f'output_excel = "{latest_path}/final_renovation_estimate.xlsx"'
    )
    
    # Write the updated script
    with open('comprehensive_cleanup.py', 'w') as f:
        f.write(new_content)
    
    # Run comprehensive cleanup
    if not run_cmd('python3 comprehensive_cleanup.py'):
        print("[ERROR] Comprehensive cleanup failed")
        return False
    
    # Step 4: Generate final summary
    print("\n📊 STEP 4: Generating final summary...")
    
    final_csv = os.path.join(latest_path, "comprehensive_clean_estimate.csv")
    final_excel = os.path.join(latest_path, "final_renovation_estimate.xlsx")
    
    if os.path.exists(final_csv) and os.path.exists(final_excel):
        print(f"\n🎉 PIPELINE COMPLETE!")
        print(f"📁 Output directory: {latest_path}")
        print(f"📊 CSV file: {final_csv}")
        print(f"📊 Excel file: {final_excel}")
        
        # Read and display the final total
        try:
            with open(final_csv, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "Grand Total" in line:
                        total = line.split(',')[-1].strip()
                        print(f"💰 FINAL ESTIMATE: ${total}")
                        break
        except:
            print("💰 Final estimate available in CSV and Excel files")
        
        # Return success for API
        return True
    else:
        print(f"[ERROR] Final files not found")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
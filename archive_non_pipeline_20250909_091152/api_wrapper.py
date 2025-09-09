#!/usr/bin/env python3
"""
API Wrapper for Renovation Estimation Pipeline
Perfect for Power Automate integration
"""

import os
import sys
import json
import subprocess
import shlex
import argparse
from datetime import datetime
import hashlib
import shutil

def run_cmd(cmd):
    """Execute a command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        return False, str(e)

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

def cleanup_old_runs(keep_last=3):
    """Clean up old run directories to save space."""
    base_dir = "chunked_outputs"
    if not os.path.exists(base_dir):
        return
    
    dirs = [d for d in os.listdir(base_dir) if d.startswith("run_")]
    if len(dirs) <= keep_last:
        return
    
    # Sort by creation time (oldest first)
    dirs.sort(key=lambda x: os.path.getctime(os.path.join(base_dir, x)))
    
    # Remove old directories
    for old_dir in dirs[:-keep_last]:
        try:
            shutil.rmtree(os.path.join(base_dir, old_dir))
            print(f"[INFO] Cleaned up old directory: {old_dir}")
        except Exception as e:
            print(f"[WARNING] Failed to clean up {old_dir}: {e}")

def validate_pipeline_output(run_dir, start_time):
    """
    Validate that the pipeline actually produced the expected output files.
    
    Args:
        run_dir (str): Path to the pipeline run directory
        start_time (datetime): When the pipeline started
    
    Returns:
        tuple: (is_valid, error_message)
    """
    start_timestamp = start_time.timestamp()
    
    # Check if run directory exists
    if not os.path.exists(run_dir):
        return False, f"Run directory not found: {run_dir}"
    
    # Check transcript chunks
    transcript_chunks_dir = os.path.join(run_dir, 'transcript_chunks')
    if not os.path.exists(transcript_chunks_dir):
        return False, "transcript_chunks directory not created"
    
    transcript_files = [f for f in os.listdir(transcript_chunks_dir) if f.endswith('.txt')]
    if not transcript_files:
        return False, "No transcript text chunks were generated"
    
    # Check GPT processing outputs
    chunk_output_files = [f for f in os.listdir(run_dir) if f.startswith('estimate_output_chunk_') and f.endswith('.txt')]
    if not chunk_output_files:
        return False, "No GPT processing output files were generated"
    
    # Check that files were created after pipeline start
    for chunk_file in chunk_output_files:
        file_path = os.path.join(run_dir, chunk_file)
        if os.path.getctime(file_path) < start_timestamp:
            return False, f"GPT output file {chunk_file} was created before pipeline start"
    
    return True, f"Pipeline validation passed: {len(transcript_files)} chunks, {len(chunk_output_files)} outputs"

def estimate_renovation(transcript_path, polycam_path, api_key, max_tokens="3000"):
    """
    Main API function for renovation estimation.
    
    Args:
        transcript_path (str): Path to transcript PDF
        polycam_path (str): Path to polycam PDF
        api_key (str): OpenAI API key
        max_tokens (str): Max tokens per chunk
    
    Returns:
        dict: JSON response with status, files, and metadata
    """
    
    start_time = datetime.now()
    
    # Initialize response
    response = {
        "status": "error",
        "message": "",
        "files": {},
        "metadata": {
            "start_time": start_time.isoformat(),
            "transcript_file": transcript_path,
            "polycam_file": polycam_path,
            "max_tokens": max_tokens
        }
    }
    
    try:
        # Validate input files
        if not os.path.exists(transcript_path):
            response["message"] = f"Transcript file not found: {transcript_path}"
            return response
        
        if not os.path.exists(polycam_path):
            response["message"] = f"Polycam file not found: {polycam_path}"
            return response
        
        print(f"[API] Starting renovation estimation for {transcript_path}")
        
        # Pre-flight check: Ensure transcript file can be read
        print("[API] Pre-flight check: Validating transcript file...")
        
        # Check file extension to determine validation method
        transcript_ext = os.path.splitext(transcript_path)[1].lower()
        
        if transcript_ext == '.pdf':
            # Validate PDF transcript
            try:
                import pdfplumber
                with pdfplumber.open(transcript_path) as pdf:
                    if len(pdf.pages) == 0:
                        response["message"] = "Transcript PDF appears to be empty or corrupted"
                        return response
                    
                    # Try to extract text from first page
                    first_page = pdf.pages[0]
                    text = first_page.extract_text()
                    if not text or len(text.strip()) < 100:
                        response["message"] = "Transcript PDF contains insufficient text for processing"
                        return response
                    
                    print(f"[API] ✅ PDF transcript validated: {len(text)} characters")
                    
            except Exception as e:
                response["message"] = f"Failed to validate transcript PDF: {str(e)}"
                return response
                
        elif transcript_ext == '.json':
            # Validate JSON transcript
            try:
                import json
                
                # Check if file is empty first
                if os.path.getsize(transcript_path) == 0:
                    response["message"] = "Transcript JSON file is empty"
                    return response
                
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                if not content:
                    response["message"] = "Transcript JSON file contains no content"
                    return response
                    
                data = json.loads(content)
                
                # Check if JSON contains meaningful content
                if isinstance(data, dict):
                    text_content = ""
                    for key, value in data.items():
                        if isinstance(value, str):
                            text_content += value + " "
                        elif isinstance(value, list):
                            text_content += " ".join(str(item) for item in value) + " "
                    
                    if len(text_content.strip()) < 50:
                        response["message"] = "Transcript JSON contains insufficient text content (minimum 50 characters required)"
                        return response
                        
                    print(f"[API] ✅ JSON transcript validated: {len(text_content)} characters")
                    
                elif isinstance(data, list):
                    text_content = " ".join(str(item) for item in data)
                    if len(text_content.strip()) < 50:
                        response["message"] = "Transcript JSON contains insufficient text content (minimum 50 characters required)"
                        return response
                        
                    print(f"[API] ✅ JSON transcript validated: {len(text_content)} characters")
                    
                else:
                    response["message"] = "Transcript JSON format not supported. Expected object or array."
                    return response
                    
            except json.JSONDecodeError as e:
                response["message"] = f"Invalid JSON format: {str(e)}. Please check your JSON file."
                return response
            except Exception as e:
                response["message"] = f"Failed to validate transcript JSON: {str(e)}"
                return response
        else:
            response["message"] = f"Unsupported transcript file type: {transcript_ext}. Only PDF and JSON files are supported."
            return response
        
        # Step 1: Running estimation pipeline...
        print("[API] Step 1: Running estimation pipeline...")
        
        # For large transcripts, show progress
        transcript_size = os.path.getsize(transcript_path)
        if transcript_size > 50000:  # 50KB
            print(f"[API] 📁 Large transcript detected: {transcript_size/1024:.1f}KB - Using optimized processing")
        
        # Set longer timeout for large files
        timeout_seconds = 600 if transcript_size > 50000 else 300
        
        # Build the pipeline command
        master_pricing_pdf = "Master Pricing Sheet - Q1 - 2025 (2).pdf"
        prompt_file = "estimation_prompt.txt"
        cmd = (
            f'source venv/bin/activate && python3 run_chunked_estimation.py '
            f'--transcript {shlex.quote(transcript_path)} '
            f'--polycam {shlex.quote(polycam_path)} '
            f'--master_pricing {shlex.quote(master_pricing_pdf)} '
            f'--prompt_file {shlex.quote(prompt_file)} '
            f'--api_key {shlex.quote(api_key)} '
            f'--max_tokens {shlex.quote(str(max_tokens))}'
        )
        print(f"[API] Executing command: {cmd}")
        
        # Ensure API key is available via environment as well
        env = os.environ.copy()
        env['OPENAI_API_KEY'] = api_key
        
        # Execute the pipeline with timeout
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=env
            )
            output = result.stdout
            print(f"[API] ✅ Pipeline execution completed. Output: {output[:200]}...")
        except subprocess.TimeoutExpired:
            response["message"] = f"Pipeline execution timed out after {timeout_seconds} seconds. Large transcript may need manual processing."
            print(f"[API] ❌ Pipeline execution timed out after {timeout_seconds} seconds")
            return response
        except subprocess.CalledProcessError as e:
            response["message"] = f"Pipeline execution failed: {e}"
            print(f"[API] ❌ Pipeline execution failed: {e}")
            return response
        
        # Additional validation: Check if the command actually created any output
        if "Estimation pipeline complete" not in output and "Next step: Run comprehensive cleanup" not in output:
            response["message"] = "Pipeline execution may have failed - missing completion indicators"
            print(f"[API] ❌ Pipeline may have failed - missing completion indicators in output")
            return response
        
        # Step 2: Find the latest output directory
        print("[API] Step 2: Finding latest output directory...")
        latest_path = find_latest_output_dir()
        if not latest_path:
            response["message"] = "No output directory found after estimation"
            return response
        
        print(f"[API] Found output directory: {latest_path}")
        
        # CRITICAL: Validate that the pipeline actually produced output files
        print("[API] Step 2.5: Validating pipeline output...")
        
        # Use the comprehensive validation function
        is_valid, validation_message = validate_pipeline_output(latest_path, start_time)
        if not is_valid:
            response["message"] = f"Pipeline validation failed: {validation_message}"
            print(f"[API] ❌ {validation_message}")
            return response
        
        print(f"[API] ✅ {validation_message}")
        
        # Step 3: Run comprehensive cleanup
        print("[API] Step 3: Running comprehensive cleanup...")
        
        # Run comprehensive cleanup directly - it will find the latest output automatically
        success, output = run_cmd('python3 comprehensive_cleanup.py')
        if not success:
            response["message"] = f"Comprehensive cleanup failed: {output}"
            print(f"[API] ❌ Comprehensive cleanup failed: {output}")
            return response
        
        print(f"[API] ✅ Comprehensive cleanup completed. Output: {output[:200]}...")
        
        # Validate that cleanup actually produced output
        if "Comprehensive cleanup completed successfully" not in output:
            response["message"] = "Comprehensive cleanup may have failed - missing completion indicators"
            print(f"[API] ❌ Comprehensive cleanup may have failed - missing completion indicators")
            print(f"[API] Cleanup output: {output[:500]}...")
            return response
        
        # Step 4: Collect results
        print("[API] Step 4: Collecting results...")
        
        # Look for the final files in the chunked_outputs directory (where cleanup script creates them)
        final_csv = None
        final_excel = None
        
        # CRITICAL: Only look for files created AFTER this pipeline started
        pipeline_start_time = start_time.timestamp()
        
        # Check for the most recent comprehensive clean CSV in the latest run directory
        if latest_path and os.path.exists(latest_path):
            csv_files = [f for f in os.listdir(latest_path) if (f.startswith('comprehensive_clean_estimate_') or f == 'comprehensive_clean_estimate.csv' or f == 'comprehensive_clean_estimate_final.csv') and f.endswith('.csv')]
            if csv_files:
                # Get the most recent CSV file that was created AFTER this pipeline started
                recent_csv_files = []
                for csv_file in csv_files:
                    file_path = os.path.join(latest_path, csv_file)
                    if os.path.getctime(file_path) > pipeline_start_time:
                        recent_csv_files.append(file_path)
                
                if recent_csv_files:
                    # Sort by creation time (newest first)
                    recent_csv_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
                    final_csv = recent_csv_files[0]
                    print(f"[API] ✅ Found new CSV file created by this pipeline: {os.path.basename(final_csv)}")
                else:
                    response["message"] = "Pipeline failed: No new CSV files were created (only old files found)"
                    return response
            
            excel_files = [f for f in os.listdir(latest_path) if (f.startswith('final_renovation_estimate_') or f == 'final_renovation_estimate.xlsx' or f == 'comprehensive_clean_estimate_final.xlsx') and f.endswith('.xlsx')]
            if excel_files:
                # Get the most recent Excel file that was created AFTER this pipeline started
                recent_excel_files = []
                for excel_file in excel_files:
                    file_path = os.path.join(latest_path, excel_file)
                    if os.path.getctime(file_path) > pipeline_start_time:
                        recent_excel_files.append(file_path)
                
                if recent_excel_files:
                    # Sort by creation time (newest first)
                    recent_excel_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
                    final_excel = recent_excel_files[0]
                    print(f"[API] ✅ Found new Excel file created by this pipeline: {os.path.basename(final_excel)}")
                else:
                    response["message"] = "Pipeline failed: No new Excel files were created (only old files found)"
                    return response
        
        if not final_csv or not final_excel:
            response["message"] = "Final files not found after cleanup"
            return response
        
        # Read final estimate
        final_total = "0"
        try:
            with open(final_csv, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if "Grand Total" in line:
                        final_total = line.split(',')[-1].strip()
                        break
        except Exception as e:
            print(f"[WARNING] Could not read final total: {e}")
        
        # Keep old runs for history (commented out cleanup)
        # cleanup_old_runs()
        
        # Success response - Simplified for Excel file only
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Convert to absolute paths for Flask app
        final_excel_abs = os.path.abspath(final_excel)
        final_csv_abs = os.path.abspath(final_csv)
        
        response = {
            "status": "success",
            "message": "Renovation estimation completed successfully",
            "files": {
                "excel_file": final_excel_abs,
                "csv_file": final_csv_abs
            },
            "metadata": {
                "duration_seconds": round(duration, 2),
                "final_estimate": final_total
            }
        }
        
        print(f"[API] ✅ Estimation completed successfully in {duration:.2f} seconds")
        print(f"[API] 📊 Final estimate: ${final_total}")
        print(f"[API] 📁 Excel file: {final_excel}")
        
        return response
        
    except Exception as e:
        response["message"] = f"Unexpected error: {str(e)}"
        return response

def main():
    """Command line interface for the API wrapper."""
    parser = argparse.ArgumentParser(description="API Wrapper for Renovation Estimation Pipeline")
    parser.add_argument("--transcript", required=True, help="Path to transcript PDF file")
    parser.add_argument("--polycam", required=True, help="Path to polycam PDF file")
    parser.add_argument("--api_key", required=True, help="OpenAI API key")
    parser.add_argument("--max_tokens", default="3000", help="Max tokens per chunk (default: 3000)")
    parser.add_argument("--output_json", help="Output JSON file path (optional)")
    
    args = parser.parse_args()
    
    # Run estimation
    result = estimate_renovation(args.transcript, args.polycam, args.api_key, args.max_tokens)
    
    # Output result
    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"[API] Results saved to: {args.output_json}")
    else:
        print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["status"] == "success" else 1)

if __name__ == "__main__":
    main() 
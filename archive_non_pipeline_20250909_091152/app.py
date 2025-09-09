#!/usr/bin/env python3
"""
Flask Web Server for Renovation Estimation API
Deployed for Power Automate integration
"""

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import shutil
from datetime import datetime
import traceback
from api_wrapper import estimate_renovation
import requests
import json # Added for JSON transcript handling
from dotenv import load_dotenv
import uuid
import threading

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Get API key from environment
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")

def load_existing_jobs():
    """Load existing job results from files when app starts."""
    try:
        jobs_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'jobs')
        if os.path.exists(jobs_dir):
            for filename in os.listdir(jobs_dir):
                if filename.endswith('.json'):
                    job_id = filename[:-5]  # Remove .json extension
                    job_file = os.path.join(jobs_dir, filename)
                    try:
                        with open(job_file, 'r') as f:
                            result = json.load(f)
                        app.config['job_results'][job_id] = result
                        print(f"[API] Loaded existing job {job_id} from file")
                    except Exception as e:
                        print(f"[API] Error loading existing job {job_id}: {e}")
    except Exception as e:
        print(f"[API] Error loading existing jobs: {e}")

# Initialize job results storage
app.config['job_results'] = {}

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'json'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "renovation-estimation-api",
        "timestamp": datetime.now().isoformat(),
        "api_key_set": bool(OPENAI_API_KEY)
    })

@app.route('/estimate', methods=['POST'])
def estimate():
    """Main endpoint for renovation estimation"""
    try:
        # Check if request is JSON or form data
        if request.is_json:
            # Handle JSON request
            data = request.get_json()
            transcript_content = data.get('transcript_json')
            polycam_base64 = data.get('polycam_base64')
            
            # Handle Power Automate's JSON wrapper format (string representation)
            if polycam_base64 and isinstance(polycam_base64, str):
                # Check if it looks like JSON
                if polycam_base64.strip().startswith('[') or polycam_base64.strip().startswith('{'):
                    try:
                        import json
                        parsed_data = json.loads(polycam_base64)
                        print(f"[DEBUG] Parsed polycam_base64 as JSON: {type(parsed_data)}")
                        
                        if isinstance(parsed_data, dict) and '$content' in parsed_data:
                            print(f"[DEBUG] Detected Power Automate JSON wrapper, extracting $content")
                            polycam_base64 = parsed_data['$content']
                        elif isinstance(parsed_data, list) and len(parsed_data) > 0:
                            if isinstance(parsed_data[0], dict) and '$content' in parsed_data[0]:
                                print(f"[DEBUG] Detected Power Automate array wrapper, extracting $content")
                                polycam_base64 = parsed_data[0]['$content']
                            else:
                                print(f"[DEBUG] WARNING: Array format but no $content found in first element")
                        else:
                            print(f"[DEBUG] WARNING: JSON parsed but no recognized format found")
                            
                    except json.JSONDecodeError as e:
                        print(f"[DEBUG] Failed to parse as JSON: {e}")
                        # Continue with original string
                else:
                    print(f"[DEBUG] polycam_base64 appears to be raw base64 string")
            
            # Handle Power Automate's JSON wrapper format (actual objects)
            elif polycam_base64 and isinstance(polycam_base64, dict):
                if '$content' in polycam_base64:
                    print(f"[DEBUG] Detected Power Automate JSON wrapper, extracting $content")
                    polycam_base64 = polycam_base64['$content']
                else:
                    print(f"[DEBUG] WARNING: polycam_base64 is dict but no $content found: {list(polycam_base64.keys())}")
            
            # Handle Power Automate's array format (actual objects)
            elif polycam_base64 and isinstance(polycam_base64, list) and len(polycam_base64) > 0:
                if isinstance(polycam_base64[0], dict) and '$content' in polycam_base64[0]:
                    print(f"[DEBUG] Detected Power Automate array wrapper, extracting $content")
                    polycam_base64 = polycam_base64[0]['$content']
                else:
                    print(f"[DEBUG] WARNING: polycam_base64 is array but no $content found in first element")
            
            print(f"[DEBUG] Received JSON request with keys: {list(data.keys())}")
            print(f"[DEBUG] Transcript content length: {len(transcript_content) if transcript_content else 'None'}")
            print(f"[DEBUG] Polycam base64 length: {len(polycam_base64) if polycam_base64 else 'None'}")
            print(f"[DEBUG] Request headers: {dict(request.headers)}")
            print(f"[DEBUG] User-Agent: {request.headers.get('User-Agent', 'Not set')}")
            print(f"[DEBUG] Accept: {request.headers.get('Accept', 'Not set')}")
            
            if not transcript_content or not polycam_base64:
                return jsonify({
                    "status": "error",
                    "message": "Missing transcript_json or polycam_base64 in JSON body"
                }), 400
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix='renovation_estimate_')
            
            try:
                # Save transcript JSON
                transcript_path = os.path.join(temp_dir, 'transcript.json')
                with open(transcript_path, 'w', encoding='utf-8') as f:
                    f.write(transcript_content)
                print(f"[DEBUG] Saved transcript JSON: {len(transcript_content)} characters")
                
                # Decode and save Polycam PDF
                polycam_path = os.path.join(temp_dir, 'polycam.pdf')
                try:
                    import base64
                    
                    # Debug the base64 string
                    print(f"[DEBUG] Base64 string starts with: {polycam_base64[:50]}...")
                    print(f"[DEBUG] Base64 string ends with: ...{polycam_base64[-50:]}")
                    print(f"[DEBUG] Base64 string contains '=' padding: {'=' in polycam_base64}")
                    
                    # Check if it looks like valid base64
                    if len(polycam_base64) % 4 != 0:
                        print(f"[DEBUG] WARNING: Base64 length {len(polycam_base64)} is not multiple of 4")
                    
                    pdf_data = base64.b64decode(polycam_base64)
                    print(f"[DEBUG] Decoded PDF data size: {len(pdf_data)} bytes")
                    print(f"[DEBUG] PDF data starts with: {pdf_data[:20].hex()}")
                    
                    # Check if it looks like a PDF
                    if pdf_data.startswith(b'%PDF'):
                        print(f"[DEBUG] ✅ PDF header detected correctly")
                    else:
                        print(f"[DEBUG] ❌ PDF header NOT detected. Starts with: {pdf_data[:20]}")
                    
                    with open(polycam_path, 'wb') as f:
                        f.write(pdf_data)
                    print(f"[DEBUG] Saved PDF file: {polycam_path} ({len(pdf_data)} bytes)")
                    
                except Exception as e:
                    print(f"[DEBUG] ❌ Base64 decode error: {str(e)}")
                    print(f"[DEBUG] Base64 string sample: {polycam_base64[:100]}...")
                    return jsonify({
                        "status": "error",
                        "message": f"Invalid base64 PDF data: {str(e)}"
                    }), 400
                
                print(f"[API] Processing JSON files: {transcript_path}, {polycam_path}")
                
                # Additional file validation
                if os.path.exists(transcript_path):
                    with open(transcript_path, 'r', encoding='utf-8') as f:
                        transcript_check = f.read()
                    print(f"[DEBUG] Transcript file validation: {len(transcript_check)} characters, starts with: {transcript_check[:100]}...")
                
                if os.path.exists(polycam_path):
                    with open(polycam_path, 'rb') as f:
                        pdf_check = f.read()
                    print(f"[DEBUG] PDF file validation: {len(pdf_check)} bytes, starts with: {pdf_check[:20].hex()}")
                    if pdf_check.startswith(b'%PDF'):
                        print(f"[DEBUG] ✅ Final PDF file has correct header")
                    else:
                        print(f"[DEBUG] ❌ Final PDF file is corrupted")
                
            except Exception as e:
                print(f"[DEBUG] ❌ General error: {str(e)}")
                shutil.rmtree(temp_dir)
                return jsonify({
                    "status": "error",
                    "message": f"Error processing JSON data: {str(e)}"
                }), 400
                
        else:
            # Handle form data request (existing logic)
            if 'transcript' not in request.files and 'transcript_json' not in request.form:
                return jsonify({
                    "status": "error",
                    "message": "Missing transcript file or transcript_json"
                }), 400
            
            if 'polycam' not in request.files:
                return jsonify({
                    "status": "error",
                    "message": "Missing polycam file"
                }), 400
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix='renovation_estimate_')
            
            try:
                # Handle transcript (file or JSON string)
                if 'transcript' in request.files:
                    transcript_file = request.files['transcript']
                    transcript_path = os.path.join(temp_dir, secure_filename(transcript_file.filename))
                    transcript_file.save(transcript_path)
                else:
                    # Handle transcript as JSON string
                    transcript_content = request.form['transcript_json']
                    transcript_path = os.path.join(temp_dir, 'transcript.json')
                    with open(transcript_path, 'w', encoding='utf-8') as f:
                        f.write(transcript_content)
                
                # Handle polycam (file or base64)
                polycam_file = request.files['polycam']
                polycam_path = os.path.join(temp_dir, secure_filename(polycam_file.filename))
                polycam_file.save(polycam_path)
                
                print(f"[API] Processing files: {transcript_path}, {polycam_path}")
                
            except Exception as e:
                shutil.rmtree(temp_dir)
                return jsonify({
                    "status": "error",
                    "message": f"Error processing form data: {str(e)}"
                }), 400
        
        # Continue with existing logic for both cases
        # Check if API key is available
        if not OPENAI_API_KEY:
            return jsonify({
                "status": "error",
                "message": "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file."
            }), 500
        
        # Check if this is a Power Automate request
        is_power_automate = 'azure-logic-apps' in request.headers.get('User-Agent', '')
        
        if is_power_automate:
            # Start async processing for Power Automate
            print(f"[API] Power Automate detected: starting async processing")
            
            # Generate unique job ID
            job_id = str(uuid.uuid4())
            
            # Initialize job results with file-based persistence
            if 'job_results' not in app.config:
                app.config['job_results'] = {}
            
            # Create jobs directory if it doesn't exist
            jobs_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'jobs')
            os.makedirs(jobs_dir, exist_ok=True)
            
            # Start background processing
            def process_async():
                try:
                    print(f"[API] [JOB {job_id}] Starting background processing...")
                    result = estimate_renovation(transcript_path, polycam_path, OPENAI_API_KEY, '3000')
                    
                    # Save result to both memory and file
                    app.config['job_results'][job_id] = result
                    
                    # Save to file for persistence
                    job_file = os.path.join(jobs_dir, f"{job_id}.json")
                    with open(job_file, 'w') as f:
                        import json
                        json.dump(result, f, indent=2)
                    
                    print(f"[API] [JOB {job_id}] ✅ Processing completed successfully")
                except Exception as e:
                    print(f"[API] [JOB {job_id}] ❌ Processing failed: {str(e)}")
                    error_result = {
                        "status": "error",
                        "error": str(e)
                    }
                    app.config['job_results'][job_id] = error_result
                    
                    # Save error to file for persistence
                    job_file = os.path.join(jobs_dir, f"{job_id}.json")
                    with open(job_file, 'w') as f:
                        import json
                        json.dump(error_result, f, indent=2)
                finally:
                    # Clean up temporary directory AFTER background processing completes
                    try:
                        if 'temp_dir' in locals():
                            shutil.rmtree(temp_dir)
                            print(f"[API] [JOB {job_id}] Cleaned up temp directory: {temp_dir}")
                    except Exception as e:
                        print(f"[API] [JOB {job_id}] WARNING: Failed to clean up temp directory: {e}")
            
            # Start background thread
            thread = threading.Thread(target=process_async)
            thread.daemon = True
            thread.start()
            
            # Return job ID immediately
            return jsonify({
                "status": "processing",
                "message": "Estimation started in background",
                "job_id": job_id,
                "poll_url": f"/estimate_status/{job_id}",
                "estimated_time": "5-7 minutes"
            }), 200
        else:
            # Process synchronously for other clients
            print(f"[API] Processing synchronously for non-Power Automate client")
            
            # Run estimation with API key from environment
            result = estimate_renovation(transcript_path, polycam_path, OPENAI_API_KEY, '3000')
            
            if result["status"] == "success":
                # Get the Excel file path from the result
                excel_file_path = result["files"].get("excel_file")

                if excel_file_path and os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):
                    # Return the Excel file directly
                    print(f"[API] Returning Excel file directly")
                    
                    # IMPORTANT: Copy file to a safe location before sending
                    # This prevents cleanup from deleting it during transfer
                    safe_file_path = os.path.join(app.config['OUTPUT_FOLDER'], "comprehensive_clean_estimate_final.xlsx")
                    shutil.copy2(excel_file_path, safe_file_path)
                    print(f"[API] Copied file to safe location: {safe_file_path}")
                    
                    return send_file(
                        safe_file_path,
                        as_attachment=True,
                        download_name="comprehensive_clean_estimate_final.xlsx",
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Excel file not found after processing",
                        "expected_path": excel_file_path
                    }), 500
            else:
                return jsonify(result), 400
            
    except Exception as e:
        print(f"[API] Error in estimate endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500
    finally:
        # Clean up temporary directory AFTER pipeline execution
        # Add small delay to ensure file transfer completes
        import time
        time.sleep(2)  # Wait 2 seconds for file transfer to complete
        
        # Only clean up for synchronous processing (not async)
        if not is_power_automate:
            try:
                if 'temp_dir' in locals():
                    shutil.rmtree(temp_dir)
                    print(f"[API] Cleaned up temp directory: {temp_dir}")
            except Exception as e:
                print(f"[WARNING] Failed to clean up temp directory: {e}")

@app.route('/estimate_status/<job_id>', methods=['GET'])
def get_estimate_status(job_id):
    """Get the status of an async estimation job."""
    try:
        job_results = app.config.get('job_results', {})
        
        # If job not in memory, try to load from file
        if job_id not in job_results:
            jobs_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'jobs')
            job_file = os.path.join(jobs_dir, f"{job_id}.json")
            
            if os.path.exists(job_file):
                try:
                    with open(job_file, 'r') as f:
                        result = json.load(f)
                    # Load into memory for future requests
                    app.config['job_results'][job_id] = result
                    job_results = app.config.get('job_results', {})
                    print(f"[API] Loaded job {job_id} from file")
                except Exception as e:
                    print(f"[API] Error loading job {job_id} from file: {e}")
                    return jsonify({
                        "status": "error",
                        "message": "Error loading job data"
                    }), 500
            else:
                return jsonify({
                    "status": "not_found",
                    "message": "Job ID not found"
                }), 404
        
        result = job_results[job_id]
        
        if result.get("status") == "success":
            # Job completed successfully, return JSON status with file info
            excel_file_path = result["files"].get("excel_file")
            
            if excel_file_path and os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):
                # Copy file to safe location
                safe_file_path = os.path.join(app.config['OUTPUT_FOLDER'], "comprehensive_clean_estimate_final.xlsx")
                shutil.copy2(excel_file_path, safe_file_path)
                print(f"[API] [JOB {job_id}] Job completed, returning status: {safe_file_path}")
                
                return jsonify({
                    "status": "success",
                    "message": "Job completed successfully",
                    "files": {
                        "excel_file": "comprehensive_clean_estimate_final.xlsx"
                    }
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "Excel file not found after successful processing"
                }), 500
        elif result.get("status") == "error":
            return jsonify({
                "status": "error",
                "message": f"Processing failed: {result.get('error', 'Unknown error')}"
            }), 500
        else:
            return jsonify({
                "status": "processing",
                "message": "Job is still processing"
            })
            
    except Exception as e:
        print(f"[API] Error in estimate_status endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500

@app.route('/estimate_file/<filename>', methods=['GET'])
def get_estimate_file(filename):
    """Get the Excel file directly by filename."""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({
                "status": "error",
                "message": "File not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"File access error: {str(e)}"
        }), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated files."""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({
                "status": "error",
                "message": "File not found"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Download error: {str(e)}"
        }), 500

@app.route('/test_excel_response', methods=['GET'])
def test_excel_response():
    """Test endpoint to return the latest Excel file as base64 JSON."""
    try:
        # Find the latest run directory
        output_dir = "chunked_outputs"
        if not os.path.exists(output_dir):
            return jsonify({"status": "error", "message": "No output directory found"}), 404
        
        # Get the most recent run directory
        run_dirs = [d for d in os.listdir(output_dir) if d.startswith('run_')]
        if not run_dirs:
            return jsonify({"status": "error", "message": "No run directories found"}), 404
        
        latest_run = max(run_dirs)
        excel_path = os.path.join(output_dir, latest_run, "comprehensive_clean_estimate_final.xlsx")
        
        if not os.path.exists(excel_path):
            return jsonify({"status": "error", "message": "Excel file not found"}), 404
        
        # Read and encode the file
        with open(excel_path, 'rb') as f:
            file_content = f.read()
        
        import base64
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        return jsonify({
            "status": "success",
            "message": "Excel file encoded successfully",
            "file_info": {
                "filename": "comprehensive_clean_estimate_final.xlsx",
                "size_bytes": len(file_content),
                "size_kb": round(len(file_content) / 1024, 2),
                "run_directory": latest_run
            },
            "file_base64": file_base64
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/files', methods=['GET'])
def list_files():
    """List available output files."""
    try:
        files = []
        output_dir = app.config['OUTPUT_FOLDER']
        
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    files.append({
                        "filename": filename,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "download_url": f"/download/{filename}"
                    })
        
        return jsonify({
            "status": "success",
            "files": files
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error listing files: {str(e)}"
        }), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation."""
    return jsonify({
        "service": "Renovation Estimation API",
        "version": "1.0.0",
        "endpoints": {
            "POST /estimate": "Submit renovation estimation request",
            "GET /health": "Health check",
            "GET /files": "List available output files",
            "GET /download/<filename>": "Download generated files",
            "GET /estimate_file/<filename>": "Get Excel file directly by filename"
        },
        "usage": {
            "method": "POST",
            "url": "/estimate",
            "content_type": "multipart/form-data",
            "parameters": {
                "transcript": "PDF file (transcript)",
                "polycam": "PDF file (polycam measurements)", 
                "api_key": "Optional: OpenAI API key (or set OPENAI_API_KEY env var)",
                "max_tokens": "Optional: Max tokens per chunk (default: 3000)",
                "return_file": "Optional: If 'true', returns Excel file directly instead of JSON response"
            }
        },
        "response_format": {
            "status": "success/error",
            "message": "Description of the result",
            "files": "File paths",
            "download_urls": "Download URLs for files",
            "file_info": {
                "excel_file": {
                    "filename": "Name of the Excel file",
                    "file_path": "Path to the file",
                    "content_type": "MIME type of the file",
                    "size_bytes": "File size in bytes",
                    "download_url": "Direct download URL"
                }
            },
            "metadata": "Processing information and timing"
        },
        "note": "The API now offers three response options: 1) JSON response with file info, 2) Direct file download when return_file=true, or 3) Use GET /estimate_file/<filename> to retrieve files directly. This eliminates the need for separate download requests and provides efficient file access."
    })

if __name__ == '__main__':
    # Set the API key if not already set
    if not os.environ.get('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = "os.getenv('OPENAI_API_KEY')"
        print("🔑 API Key set from default")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Renovation Estimation API on port {port}")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"📁 Output folder: {app.config['OUTPUT_FOLDER']}")
    print(f"🌐 Health check: http://localhost:{port}/health")
    print(f"🔑 API Key: {os.environ.get('OPENAI_API_KEY', 'NOT SET')[:20]}...")
    
    # Load existing jobs from files
    load_existing_jobs()
    
    app.run(host='0.0.0.0', port=port, debug=debug) 
#!/usr/bin/env python3
"""
FastAPI Web Server for Renovation Estimation API
Deployed for Power Automate integration
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import tempfile
import shutil
from datetime import datetime
import traceback
from archive_non_pipeline_20250909_091152.api_wrapper import estimate_renovation
import requests
import json
from werkzeug.utils import secure_filename
import base64
import uuid
import threading
import time

app = FastAPI(
    title="Renovation Estimation API",
    description="API for processing renovation estimates from transcripts and polycam measurements",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Job storage for async processing
jobs = {}  # In production, use Redis or database

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'json'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_estimation_async(job_id, transcript_path, polycam_path, api_key, max_tokens):
    """Process estimation in background thread."""
    try:
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['message'] = 'Starting estimation...'
        
        result = estimate_renovation(transcript_path, polycam_path, api_key, str(max_tokens))
        
        if result["status"] == "success":
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['result'] = result
            jobs[job_id]['message'] = 'Estimation completed successfully'
        else:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = result.get("message", "Estimation failed")
            
    except Exception as e:
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = f"Error: {str(e)}"
    finally:
        jobs[job_id]['completed_at'] = datetime.now().isoformat()

# Pydantic models for request/response
class FlexibleEstimateRequest(BaseModel):
    # Transcript inputs
    transcript_json: Optional[dict] = None
    transcript_url: Optional[str] = None
    transcript_base64: Optional[str] = None  # base64-encoded JSON text
    # Polycam inputs
    polycam_url: Optional[str] = None
    polycam_base64: Optional[str] = None  # base64-encoded PDF bytes
    # Controls
    api_key: Optional[str] = None
    max_tokens: Optional[int] = 3000
    response_mode: Optional[str] = "json"  # json | file | base64

class EstimationResponse(BaseModel):
    status: str
    message: str
    files: Optional[dict] = None
    download_urls: Optional[dict] = None
    file_info: Optional[dict] = None
    metadata: Optional[dict] = None

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "renovation-estimation-api",
        "timestamp": datetime.now().isoformat(),
        "api_key_set": bool(os.environ.get('OPENAI_API_KEY'))
    }

# Multipart/form-data endpoint (kept for compatibility with PA file uploads)
@app.post("/estimate", response_model=EstimationResponse)
async def estimate(
    transcript: Optional[UploadFile] = File(None),
    polycam: Optional[UploadFile] = File(None),
    transcript_json: Optional[str] = Form(None),
    polycam_url: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    max_tokens: Optional[int] = Form(3000),
    return_file: Optional[bool] = Form(False),
    response_mode: Optional[str] = Form(None)
):
    """
    Main estimation endpoint.
    
    Expected form data:
    - transcript: PDF file (transcript)
    - polycam: PDF file (polycam measurements)
    - transcript_json: JSON transcript data (alternative to transcript file)
    - polycam_url: URL to polycam PDF (alternative to polycam file)
    - api_key: OpenAI API key
    - max_tokens: Max tokens per chunk
    - return_file: If true, returns file directly instead of JSON
    
    Returns:
    - JSON response with status and file info, OR
    - Direct file download if return_file=true
    """
    
    try:
        temp_dir = tempfile.mkdtemp(prefix='renovation_estimate_')
        transcript_path = None
        polycam_path = None

        try:
            # Handle transcript input
            if transcript_json:
                # Parse JSON transcript data
                try:
                    transcript_data = json.loads(transcript_json)
                    transcript_path = os.path.join(temp_dir, 'transcript.json')
                    with open(transcript_path, 'w', encoding='utf-8') as f:
                        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
                    print(f"[API] Created transcript from JSON data: {transcript_path}")
                except json.JSONDecodeError:
                    raise HTTPException(status_code=400, detail="Invalid JSON in transcript_json field.")
            elif transcript:
                # Handle uploaded transcript file
                if not allowed_file(transcript.filename):
                    raise HTTPException(status_code=400, detail="Invalid transcript file type. Only PDF and JSON files are allowed.")
                
                transcript_path = os.path.join(temp_dir, secure_filename(transcript.filename))
                with open(transcript_path, 'wb') as f:
                    shutil.copyfileobj(transcript.file, f)
            else:
                raise HTTPException(status_code=400, detail="Missing transcript. Upload 'transcript' file or provide 'transcript_json' data.")

            # Handle polycam input
            if polycam:
                # Handle uploaded polycam file
                if not allowed_file(polycam.filename):
                    raise HTTPException(status_code=400, detail="Invalid polycam file type. Only PDF files are allowed.")
                
                polycam_path = os.path.join(temp_dir, secure_filename(polycam.filename))
                with open(polycam_path, 'wb') as f:
                    shutil.copyfileobj(polycam.file, f)
            elif polycam_url:
                # Download polycam from URL
                try:
                    r = requests.get(polycam_url, stream=True, timeout=60)
                    r.raise_for_status()
                    polycam_path = os.path.join(temp_dir, 'polycam.pdf')
                    with open(polycam_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to download polycam from URL: {str(e)}")
            else:
                raise HTTPException(status_code=400, detail="Missing polycam. Upload 'polycam' file or provide 'polycam_url'.")

            # Set API key
            if not api_key:
                api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="No API key provided. Set OPENAI_API_KEY environment variable or pass api_key.")

            print(f"[API] Processing files: {transcript_path}, {polycam_path}")

            # Run estimation
            result = estimate_renovation(transcript_path, polycam_path, api_key, str(max_tokens))

            if result["status"] == "success":
                # Copy only the Excel file to accessible location
                excel_file_path = result["files"].get("excel_file")
                
                if excel_file_path and os.path.exists(excel_file_path) and os.path.isfile(excel_file_path):
                    # Create a unique filename for this request
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.basename(excel_file_path)
                    name, ext = os.path.splitext(filename)
                    new_filename = f"{name}_{timestamp}{ext}"
                    new_path = os.path.join(OUTPUT_FOLDER, new_filename)
                    
                    # Copy Excel file to output directory
                    shutil.copy2(excel_file_path, new_path)
                    
                    # Response selection (response_mode has priority)
                    mode = (response_mode or ("file" if return_file else "json")).lower()
                    if mode == "file":
                        print(f"[API] Returning Excel file directly: {new_path}")
                        return FileResponse(
                            path=new_path,
                            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            filename=new_filename
                        )
                    elif mode == "base64":
                        with open(new_path, 'rb') as fh:
                            payload = base64.b64encode(fh.read()).decode('utf-8')
                        return {
                            "status": "success",
                            "message": "Renovation estimation completed successfully",
                            "file_base64": payload,
                            "filename": new_filename,
                            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "metadata": {"created": datetime.now().isoformat()}
                        }
                    
                    # Otherwise, return file info for JSON response
                    result["files"] = {"excel_file": new_filename}
                    result["download_urls"] = {
                        "excel_file": f"/download/{new_filename}"
                    }
                    result["file_info"] = {
                        "excel_file": {
                            "filename": new_filename,
                            "file_path": new_path,
                            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "size_bytes": os.path.getsize(new_path),
                            "download_url": f"/download/{new_filename}"
                        }
                    }
                    
                    print(f"[API] Copied Excel file to: {new_path} and prepared for response")
                else:
                    raise HTTPException(status_code=400, detail="Excel file not found after estimation")
                
                return result
            else:
                raise HTTPException(status_code=400, detail=result.get("message", "Estimation failed"))
                
        finally:
            # Clean up temporary directory
            try:
                shutil.rmtree(temp_dir)
                print(f"[API] Cleaned up temp directory: {temp_dir}")
            except Exception as e:
                print(f"[WARNING] Failed to clean up temp directory: {e}")
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(traceback.format_exc())
        
        raise HTTPException(status_code=500, detail=error_msg)

# JSON endpoint to avoid multipart boundary issues
@app.post("/estimate_json")
async def estimate_json(payload: FlexibleEstimateRequest = Body(...)):
    try:
        temp_dir = tempfile.mkdtemp(prefix='renovation_estimate_')
        transcript_path = None
        polycam_path = None

        try:
            # Transcript resolution
            if payload.transcript_json is not None:
                transcript_path = os.path.join(temp_dir, 'transcript.json')
                with open(transcript_path, 'w', encoding='utf-8') as f:
                    json.dump(payload.transcript_json, f, indent=2, ensure_ascii=False)
            elif payload.transcript_base64:
                try:
                    text = base64.b64decode(payload.transcript_base64.encode('utf-8')).decode('utf-8')
                    data = json.loads(text)
                    transcript_path = os.path.join(temp_dir, 'transcript.json')
                    with open(transcript_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid transcript_base64 (must be base64-encoded JSON text)")
            elif payload.transcript_url:
                try:
                    r = requests.get(payload.transcript_url, timeout=60)
                    r.raise_for_status()
                    # If URL returns JSON text
                    try:
                        data = r.json()
                        transcript_path = os.path.join(temp_dir, 'transcript.json')
                        with open(transcript_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                    except ValueError:
                        # Fallback: save as file
                        transcript_path = os.path.join(temp_dir, 'transcript.json')
                        with open(transcript_path, 'wb') as f:
                            f.write(r.content)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to fetch transcript_url: {str(e)}")
            else:
                raise HTTPException(status_code=400, detail="Provide transcript_json, transcript_base64, or transcript_url")

            # Polycam resolution
            if payload.polycam_base64:
                try:
                    pdf_bytes = base64.b64decode(payload.polycam_base64.encode('utf-8'))
                    polycam_path = os.path.join(temp_dir, 'polycam.pdf')
                    with open(polycam_path, 'wb') as f:
                        f.write(pdf_bytes)
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid polycam_base64 (must be base64-encoded PDF)")
            elif payload.polycam_url:
                try:
                    r = requests.get(payload.polycam_url, stream=True, timeout=60)
                    r.raise_for_status()
                    polycam_path = os.path.join(temp_dir, 'polycam.pdf')
                    with open(polycam_path, 'wb') as f:
                        for chunk in r.iter_content(8192):
                            if chunk:
                                f.write(chunk)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to download polycam_url: {str(e)}")
            else:
                raise HTTPException(status_code=400, detail="Provide polycam_url or polycam_base64")

            # API key and options
            api_key = payload.api_key or os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="No API key provided. Set OPENAI_API_KEY or pass api_key")

            print(f"[API] Processing files: {transcript_path}, {polycam_path}")
            result = estimate_renovation(transcript_path, polycam_path, api_key, str(payload.max_tokens or 3000))

            if result.get("status") != "success":
                raise HTTPException(status_code=400, detail=result.get("message", "Estimation failed"))

            excel_file_path = result["files"].get("excel_file")
            if not excel_file_path or not os.path.exists(excel_file_path):
                raise HTTPException(status_code=400, detail="Excel file not found after estimation")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(excel_file_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{timestamp}{ext}"
            new_path = os.path.join(OUTPUT_FOLDER, new_filename)
            shutil.copy2(excel_file_path, new_path)

            mode = (payload.response_mode or "json").lower()
            if mode == "file":
                return FileResponse(
                    path=new_path,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    filename=new_filename
                )
            if mode == "base64":
                with open(new_path, 'rb') as fh:
                    payload_b64 = base64.b64encode(fh.read()).decode('utf-8')
                return {
                    "status": "success",
                    "message": "Renovation estimation completed successfully",
                    "file_base64": payload_b64,
                    "filename": new_filename,
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }

            # default json
            return {
                "status": "success",
                "message": "Renovation estimation completed successfully",
                "files": {"excel_file": new_filename},
                "download_urls": {"excel_file": f"/download/{new_filename}"},
                "metadata": {"created": datetime.now().isoformat()}
            }

        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Add Flask-style file upload endpoint
@app.post("/estimate_files")
async def estimate_files(
    transcript: UploadFile = File(...),
    polycam: UploadFile = File(...),
    api_key: Optional[str] = Form(None),
    max_tokens: Optional[int] = Form(3000),
    response_mode: Optional[str] = Form("json")
):
    """
    Flask-style file upload endpoint that accepts actual PDF files.
    This mimics how Flask handled the files and should work identically.
    """
    try:
        temp_dir = tempfile.mkdtemp(prefix='renovation_estimate_')
        transcript_path = None
        polycam_path = None

        try:
            # Save uploaded files directly (like Flask does)
            transcript_path = os.path.join(temp_dir, 'transcript.pdf')
            with open(transcript_path, 'wb') as f:
                shutil.copyfileobj(transcript.file, f)
            
            polycam_path = os.path.join(temp_dir, 'polycam.pdf')
            with open(polycam_path, 'wb') as f:
                shutil.copyfileobj(polycam.file, f)
            
            print(f"[API] Files uploaded: transcript={transcript.filename}, polycam={polycam.filename}")
            print(f"[API] File sizes: transcript={os.path.getsize(transcript_path)} bytes, polycam={os.path.getsize(polycam_path)} bytes")

            # API key and options
            api_key = api_key or os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="No API key provided. Set OPENAI_API_KEY or pass api_key")

            print(f"[API] Processing files: {transcript_path}, {polycam_path}")
            result = estimate_renovation(transcript_path, polycam_path, api_key, str(max_tokens))

            if result.get("status") != "success":
                raise HTTPException(status_code=400, detail=result.get("message", "Estimation failed"))

            excel_file_path = result["files"].get("excel_file")
            if not excel_file_path or not os.path.exists(excel_file_path):
                raise HTTPException(status_code=400, detail="Excel file not found after estimation")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(excel_file_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{timestamp}{ext}"
            new_path = os.path.join(OUTPUT_FOLDER, new_filename)
            shutil.copy2(excel_file_path, new_path)

            mode = (response_mode or "json").lower()
            if mode == "file":
                return FileResponse(
                    path=new_path,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    filename=new_filename
                )
            if mode == "base64":
                with open(new_path, 'rb') as fh:
                    payload_b64 = base64.b64encode(fh.read()).decode('utf-8')
                return {
                    "status": "success",
                    "message": "Renovation estimation completed successfully",
                    "file_base64": payload_b64,
                    "filename": new_filename,
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }

            # default json
            return {
                "status": "success",
                "message": "Renovation estimation completed successfully",
                "files": {"excel_file": new_filename},
                "download_urls": {"excel_file": f"/download/{new_filename}"},
                "metadata": {"created": datetime.now().isoformat()}
            }

        finally:
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/estimate_file/{filename}")
async def get_estimate_file(filename: str):
    """Get the Excel file directly by filename."""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=filename
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File access error: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files."""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                media_type="application/octet-stream",
                filename=filename
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download error: {str(e)}")

@app.get("/files")
async def list_files():
    """List available output files."""
    try:
        files = []
        output_dir = OUTPUT_FOLDER
        
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
        
        return {
            "status": "success",
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

# Async estimation endpoints
@app.post("/estimate_async")
async def estimate_async(payload: FlexibleEstimateRequest = Body(...)):
    """Submit async estimation request - returns job ID immediately."""
    try:
        job_id = str(uuid.uuid4())
        
        # Prepare files
        temp_dir = tempfile.mkdtemp(prefix=f'async_estimate_{job_id}_')
        transcript_path = None
        polycam_path = None

        try:
            # Transcript resolution (same as estimate_json)
            if payload.transcript_json is not None:
                transcript_path = os.path.join(temp_dir, 'transcript.json')
                with open(transcript_path, 'w', encoding='utf-8') as f:
                    json.dump(payload.transcript_json, f, indent=2, ensure_ascii=False)
            elif payload.transcript_base64:
                try:
                    text = base64.b64decode(payload.transcript_base64.encode('utf-8')).decode('utf-8')
                    data = json.loads(text)
                    transcript_path = os.path.join(temp_dir, 'transcript.json')
                    with open(transcript_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid transcript_base64")
            elif payload.transcript_url:
                try:
                    r = requests.get(payload.transcript_url, timeout=60)
                    r.raise_for_status()
                    try:
                        data = r.json()
                        transcript_path = os.path.join(temp_dir, 'transcript.json')
                        with open(transcript_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                    except ValueError:
                        transcript_path = os.path.join(temp_dir, 'transcript.json')
                        with open(transcript_path, 'wb') as f:
                            f.write(r.content)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to fetch transcript_url: {str(e)}")
            else:
                raise HTTPException(status_code=400, detail="Provide transcript_json, transcript_base64, or transcript_url")

            # Polycam resolution (same as estimate_json)
            if payload.polycam_base64:
                try:
                    pdf_bytes = base64.b64decode(payload.polycam_base64.encode('utf-8'))
                    polycam_path = os.path.join(temp_dir, 'polycam.pdf')
                    with open(polycam_path, 'wb') as f:
                        f.write(pdf_bytes)
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid polycam_base64")
            elif payload.polycam_url:
                try:
                    r = requests.get(payload.polycam_url, stream=True, timeout=60)
                    r.raise_for_status()
                    polycam_path = os.path.join(temp_dir, 'polycam.pdf')
                    with open(polycam_path, 'wb') as f:
                        for chunk in r.iter_content(8192):
                            if chunk:
                                f.write(chunk)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to download polycam_url: {str(e)}")
            else:
                raise HTTPException(status_code=400, detail="Provide polycam_url or polycam_base64")

            # API key
            api_key = payload.api_key or os.environ.get('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="No API key provided")

            # Initialize job
            jobs[job_id] = {
                'status': 'queued',
                'message': 'Job queued for processing',
                'created_at': datetime.now().isoformat(),
                'temp_dir': temp_dir,
                'transcript_path': transcript_path,
                'polycam_path': polycam_path,
                'api_key': api_key,
                'max_tokens': payload.max_tokens or 3000
            }

            # Start background processing
            thread = threading.Thread(
                target=process_estimation_async,
                args=(job_id, transcript_path, polycam_path, api_key, payload.max_tokens or 3000)
            )
            thread.daemon = True
            thread.start()

            return {
                "status": "queued",
                "job_id": job_id,
                "message": "Estimation job queued successfully",
                "check_status_url": f"/status/{job_id}",
                "get_result_url": f"/result/{job_id}"
            }

        except HTTPException:
            # Clean up temp directory on error
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            raise
        except Exception as e:
            # Clean up temp directory on error
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            raise HTTPException(status_code=500, detail=f"Error setting up async job: {str(e)}")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """Get the status of an async estimation job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job['status'],
        "message": job['message'],
        "created_at": job['created_at'],
        "completed_at": job.get('completed_at')
    }

@app.get("/result/{job_id}")
async def get_job_result(job_id: str, include_base64: bool = False):
    """Get the result of a completed async estimation job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job['status'] == 'queued':
        raise HTTPException(status_code=202, detail="Job is still queued")
    elif job['status'] == 'processing':
        raise HTTPException(status_code=202, detail="Job is still processing")
    elif job['status'] == 'failed':
        raise HTTPException(status_code=400, detail=f"Job failed: {job['message']}")
    elif job['status'] == 'completed':
        result = job['result']
        
        # Copy Excel file to accessible location
        excel_file_path = result["files"].get("excel_file")
        if excel_file_path and os.path.exists(excel_file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(excel_file_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{job_id}_{timestamp}{ext}"
            new_path = os.path.join(OUTPUT_FOLDER, new_filename)
            
            shutil.copy2(excel_file_path, new_path)
            
            response_data = {
                "status": "success",
                "message": "Estimation completed successfully",
                "files": {"excel_file": new_filename},
                "download_urls": {"excel_file": f"/download/{new_filename}"},
                "metadata": result.get("metadata", {})
            }
            
            # Include base64 content if requested
            if include_base64:
                try:
                    with open(new_path, 'rb') as f:
                        file_content = f.read()
                        file_base64 = base64.b64encode(file_content).decode('utf-8')
                        response_data["files"]["excel_file_base64"] = file_base64
                except Exception as e:
                    response_data["error"] = f"Failed to encode file: {str(e)}"
            
            # Clean up temp directory
            try:
                shutil.rmtree(job['temp_dir'])
            except:
                pass
            
            return response_data
        else:
            raise HTTPException(status_code=500, detail="Excel file not found in result")
    else:
        raise HTTPException(status_code=500, detail=f"Unknown job status: {job['status']}")

@app.get("/")
async def index():
    """API documentation."""
    return {
        "service": "Renovation Estimation API (FastAPI)",
        "version": "1.0.0",
        "endpoints": {
            "POST /estimate": "Submit renovation estimation request (multipart/form-data)",
            "POST /estimate_json": "Submit renovation estimation request (JSON body)",
            "POST /estimate_async": "Submit async renovation estimation request (returns job ID immediately)",
            "GET /status/{job_id}": "Check status of async estimation job",
            "GET /result/{job_id}": "Get results of completed estimation job",
            "GET /health": "Health check",
            "GET /files": "List available output files",
            "GET /download/<filename>": "Download generated files",
            "GET /estimate_file/<filename>": "Get Excel file directly by filename"
        },
        "usage": {
            "multipart_endpoint": {
                "method": "POST",
                "url": "/estimate",
                "content_type": "multipart/form-data",
                "parameters": {
                    "transcript": "PDF file (transcript)",
                    "polycam": "PDF file (polycam measurements)", 
                    "transcript_json": "JSON transcript data (alternative to transcript file)",
                    "polycam_url": "URL to polycam PDF (alternative to polycam file)",
                    "api_key": "Optional: OpenAI API key (or set OPENAI_API_KEY env var)",
                    "max_tokens": "Optional: Max tokens per chunk (default: 3000)",
                    "return_file": "Optional: If 'true', returns Excel file directly instead of JSON response",
                    "response_mode": "Optional: json | file | base64 (overrides return_file)"
                }
            },
            "json_endpoint": {
                "method": "POST",
                "url": "/estimate_json",
                "content_type": "application/json",
                "parameters": {
                    "transcript_json": "JSON transcript data (dict)",
                    "transcript_base64": "Base64-encoded JSON text (alternative to transcript_json)",
                    "transcript_url": "URL to JSON transcript (alternative to transcript_json)",
                    "polycam_base64": "Base64-encoded PDF bytes",
                    "polycam_url": "URL to polycam PDF (alternative to polycam_base64)",
                    "api_key": "Optional: OpenAI API key (or set OPENAI_API_KEY env var)",
                    "max_tokens": "Optional: Max tokens per chunk (default: 3000)",
                    "response_mode": "json | file | base64 (default: json)"
                }
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
    }

if __name__ == '__main__':
    import uvicorn
    
    # Set the API key if not already set
    if not os.environ.get('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = "os.getenv('OPENAI_API_KEY')"
        print("🔑 API Key set from default")
    
    # Run the FastAPI app
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting Renovation Estimation API (FastAPI) on port {port}")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"📁 Output folder: {OUTPUT_FOLDER}")
    print(f"🌐 Health check: http://localhost:{port}/health")
    print(f"🔑 API Key: {os.environ.get('OPENAI_API_KEY', 'NOT SET')[:20]}...")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

# Renovation Estimation API - Usage Guide

## Overview
The Renovation Estimation API now supports **transcript.txt** files in addition to PDF and JSON formats.

## Supported Transcript Formats
- **PDF** (.pdf) - Scanned or digital transcript documents
- **JSON** (.json) - Structured transcript data
- **TXT** (.txt) - Plain text transcripts (NEW!)

## API Endpoints

### 1. Multipart Form Upload - `/estimate`
Upload files directly using multipart/form-data.

**Supported transcript formats:** PDF, JSON, TXT

```bash
curl -X POST https://your-api-url.com/estimate \
  -F "transcript=@transcript.txt" \
  -F "polycam=@polycam.pdf" \
  -F "response_mode=json"
```

### 2. JSON Endpoint - `/estimate_json`
Send data as JSON with base64-encoded content or URLs.

**Example with base64-encoded text:**
```bash
# Encode your transcript.txt to base64
TRANSCRIPT_BASE64=$(base64 -i transcript.txt)

curl -X POST https://your-api-url.com/estimate_json \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_base64": "'$TRANSCRIPT_BASE64'",
    "polycam_url": "https://example.com/polycam.pdf",
    "response_mode": "json"
  }'
```

**Example with URL:**
```bash
curl -X POST https://your-api-url.com/estimate_json \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_url": "https://example.com/transcript.txt",
    "polycam_url": "https://example.com/polycam.pdf",
    "response_mode": "json"
  }'
```

### 3. Async Endpoint - `/estimate_async`
Submit a job and get results later (recommended for large files).

```bash
# Submit job
curl -X POST https://your-api-url.com/estimate_async \
  -H "Content-Type: application/json" \
  -d '{
    "transcript_url": "https://example.com/transcript.txt",
    "polycam_url": "https://example.com/polycam.pdf"
  }'

# Response: {"job_id": "abc-123", "status": "queued", ...}

# Check status
curl https://your-api-url.com/status/abc-123

# Get result when complete
curl https://your-api-url.com/result/abc-123
```

## Response Modes

- **json** (default) - Returns JSON with download URLs
- **file** - Returns Excel file directly
- **base64** - Returns base64-encoded Excel file in JSON

## Power Automate Integration

### Using transcript.txt with Power Automate

1. **Get File Content** action to read your transcript.txt
2. **HTTP** action to call the API:
   - Method: POST
   - URI: `https://your-api-url.com/estimate_json`
   - Headers: `Content-Type: application/json`
   - Body:
   ```json
   {
     "transcript_base64": "@{base64(body('Get_file_content'))}",
     "polycam_url": "YOUR_POLYCAM_URL",
     "response_mode": "base64"
   }
   ```

3. **Parse JSON** to extract the base64 file content
4. **Create File** to save the Excel output

## Local Pipeline Usage

Run the complete pipeline locally with a .txt transcript:

```bash
python3 run_chunked_estimation.py \
  --transcript transcript.txt \
  --polycam polycam.pdf \
  --api_key YOUR_OPENAI_API_KEY \
  --max_tokens 10000
```

## Testing

Test transcript processing:
```bash
python3 process_transcript.py transcript.txt \
  --output_dir test_chunks \
  --max_tokens 3000
```

## Notes

- The API automatically detects whether the transcript is JSON or plain text
- Plain text transcripts are processed the same way as JSON transcripts
- All existing functionality remains unchanged - this is a backward-compatible update
- Maximum file size: 50MB
- Recommended chunk size: 3000-10000 tokens depending on transcript complexity

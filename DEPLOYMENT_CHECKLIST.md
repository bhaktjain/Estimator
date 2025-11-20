# Deployment Checklist - TXT Transcript Support

## Changes Made

### 1. Updated `process_transcript.py`
- ✅ Added `process_txt_transcript()` function to handle plain text files
- ✅ Updated `process_transcript()` to route .txt files to the new handler
- ✅ Updated help text to mention TXT support

### 2. Updated `archive_non_pipeline_20250909_091152/app_fastapi.py`
- ✅ Added 'txt' to `ALLOWED_EXTENSIONS`
- ✅ Updated `/estimate` endpoint to accept TXT files
- ✅ Updated `/estimate_json` endpoint to auto-detect JSON vs plain text
- ✅ Updated `/estimate_async` endpoint to handle TXT files
- ✅ Updated API documentation strings
- ✅ Enhanced base64 decoding to handle both JSON and plain text

### 3. Updated `run_chunked_estimation.py`
- ✅ Added .txt to supported file extensions check

### 4. Documentation
- ✅ Created `API_USAGE.md` with examples for .txt files
- ✅ Created `test_txt_support.py` for validation
- ✅ All tests passing

## Deployment Steps

### For Render.com

1. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Add support for transcript.txt files"
   git push origin main
   ```

2. **Render will auto-deploy** (if auto-deploy is enabled in render.yaml)
   - Monitor deployment at: https://dashboard.render.com

3. **Verify deployment:**
   ```bash
   curl https://your-app.onrender.com/health
   ```

### For Local Testing

1. **Start the server:**
   ```bash
   python3 archive_non_pipeline_20250909_091152/app_fastapi.py
   ```

2. **Test with a .txt file:**
   ```bash
   curl -X POST http://localhost:5000/estimate \
     -F "transcript=@transcript.txt" \
     -F "polycam=@polycam.pdf" \
     -F "response_mode=json"
   ```

## Verification Tests

### Test 1: Process Transcript
```bash
python3 test_txt_support.py
```
Expected: All tests pass ✅

### Test 2: API Health Check
```bash
curl https://your-api-url.com/health
```
Expected: `{"status": "healthy", ...}`

### Test 3: Upload TXT File
```bash
curl -X POST https://your-api-url.com/estimate \
  -F "transcript=@test_transcript.txt" \
  -F "polycam=@polycam.pdf"
```
Expected: Successful estimation response

### Test 4: JSON Endpoint with Base64 TXT
```bash
TRANSCRIPT_BASE64=$(base64 -i transcript.txt)
curl -X POST https://your-api-url.com/estimate_json \
  -H "Content-Type: application/json" \
  -d "{\"transcript_base64\": \"$TRANSCRIPT_BASE64\", \"polycam_url\": \"URL\"}"
```
Expected: Successful estimation response

## Backward Compatibility

✅ All existing functionality preserved:
- PDF transcripts still work
- JSON transcripts still work
- All API endpoints unchanged
- Response formats unchanged

## Environment Variables

Ensure these are set in Render:
- `OPENAI_API_KEY` - Your OpenAI API key
- `PYTHON_VERSION` - 3.11.9 (as specified in render.yaml)
- `WEB_CONCURRENCY` - 1 (as specified in render.yaml)

## Rollback Plan

If issues occur:
```bash
git revert HEAD
git push origin main
```

Render will auto-deploy the previous version.

## Support

For issues or questions:
1. Check logs in Render dashboard
2. Review `API_USAGE.md` for usage examples
3. Run `python3 test_txt_support.py` locally to verify setup

## Status

- [x] Code changes complete
- [x] Tests passing
- [x] Documentation created
- [ ] Deployed to Render
- [ ] Production verification complete

# Monitoring Guide - Power Automate Integration

## Understanding the Logs

When your Power Automate flow runs, you'll see logs like this in Render:

```
[API] Starting renovation estimation for /tmp/async_estimate_XXX/transcript.txt
[API] Pre-flight check: Validating transcript file...
[API] ✅ TXT transcript validated: 1234 characters
[API] Step 1: Running estimation pipeline...
[API] Transcript: /tmp/async_estimate_XXX/transcript.txt (.txt)
[API] Polycam: /tmp/async_estimate_XXX/polycam.pdf
[API] Transcript size: 1234 bytes (1.2KB)
[API] Executing command: python3 run_chunked_estimation.py...
[API] ✅ Pipeline execution completed
[API] Step 2: Finding latest output directory...
[API] Found output directory: chunked_outputs/run_20251121_XXXXXX
[API] Step 2.5: Validating pipeline output...
[API] ✅ Pipeline validation passed: 3 chunks, 3 outputs
[API] Step 3: Running comprehensive cleanup...
[API] ✅ Comprehensive cleanup completed
[API] Step 4: Collecting results...
[API] ✅ Found new Excel file created by this pipeline: final_renovation_estimate_XXXXX.xlsx
[API] ✅ Estimation completed successfully in 45.23 seconds
[API] 📊 Final estimate: $12,345.67
[API] 📁 Excel file: /path/to/file.xlsx
```

## What Each Step Means

### Step 1: Validation
```
[API] Pre-flight check: Validating transcript file...
[API] ✅ TXT transcript validated: 1234 characters
```
- Checks if the transcript file is valid
- For TXT: Ensures it has at least 50 characters
- For JSON: Validates JSON structure
- For PDF: Checks if text can be extracted

**If this fails:** Your transcript file is empty, corrupted, or too short

### Step 2: Pipeline Execution
```
[API] Step 1: Running estimation pipeline...
[API] Executing command: python3 run_chunked_estimation.py...
```
- Runs the main estimation pipeline
- Processes transcript into chunks
- Sends chunks to GPT for analysis
- Can take 30-120 seconds depending on transcript size

**If this fails:** Check OpenAI API key, transcript format, or API rate limits

### Step 3: Output Validation
```
[API] Step 2.5: Validating pipeline output...
[API] ✅ Pipeline validation passed: 3 chunks, 3 outputs
```
- Verifies that GPT actually processed the chunks
- Ensures output files were created

**If this fails:** GPT processing failed or timed out

### Step 4: Cleanup
```
[API] Step 3: Running comprehensive cleanup...
[API] ✅ Comprehensive cleanup completed
```
- Aggregates all chunk outputs
- Creates final Excel file
- Applies pricing and formatting

**If this fails:** Check comprehensive_cleanup.py logs

### Step 5: Results
```
[API] ✅ Estimation completed successfully in 45.23 seconds
[API] 📊 Final estimate: $12,345.67
```
- Shows total processing time
- Shows final estimate amount
- Returns Excel file path

## Common Issues and Solutions

### Issue 1: Job Stays in "processing" Status Forever

**Symptoms:**
- Your Power Automate loop keeps checking status
- Status never changes to "completed"
- Render logs show the job started but no completion

**Causes:**
1. Pipeline crashed without updating job status
2. OpenAI API timeout
3. Out of memory

**Solution:**
Check Render logs for errors. Look for:
- `[API] ❌` messages
- Python exceptions
- Memory errors

### Issue 2: "Invalid transcript_base64" Error

**Symptoms:**
```json
{"detail": "Invalid transcript_base64"}
```

**Cause:**
The base64 string is malformed or not UTF-8

**Solution:**
In Power Automate, use:
```
@{base64(body('Get_file_content'))}
```

NOT:
```
@{body('Get_file_content')}
```

### Issue 3: Job Completes But No File

**Symptoms:**
- Status shows "completed"
- But no Excel file in response

**Cause:**
Pipeline validation failed or cleanup didn't run

**Solution:**
Check logs for:
```
[API] ❌ Pipeline validation failed
```

### Issue 4: Timeout in Power Automate

**Symptoms:**
- Power Automate flow times out
- Job is still processing

**Cause:**
Large transcript takes longer than your timeout setting

**Solution:**
1. Increase timeout in "Do until" loop (currently PT1H = 1 hour)
2. Increase delay between status checks (currently 10 seconds)
3. Use smaller transcript chunks

## Recommended Power Automate Settings

### Do Until Loop
```
Loop until: @equals(body('Status')?['status'], 'completed')
Count: 60 (checks)
Timeout: PT1H (1 hour)
```

### Delay Between Checks
```
Interval: 10 seconds
```

This means:
- Check status every 10 seconds
- Maximum 60 checks = 10 minutes total
- Timeout after 1 hour as safety

## Monitoring in Render

### View Live Logs
1. Go to https://dashboard.render.com
2. Select your service: "Estimator"
3. Click "Logs" tab
4. Watch for `[API]` messages

### Check for Errors
Look for these patterns:
- `[API] ❌` - Error occurred
- `[ERROR]` - Python error
- `Failed to` - Operation failed
- `Timeout` - Process timed out

### Successful Run Pattern
```
[API] Starting renovation estimation
[API] ✅ TXT transcript validated
[API] ✅ Pipeline execution completed
[API] ✅ Pipeline validation passed
[API] ✅ Comprehensive cleanup completed
[API] ✅ Estimation completed successfully
```

## Debugging Steps

### Step 1: Check Job Status
```bash
curl https://estimator-bb7k.onrender.com/status/YOUR_JOB_ID
```

Expected response:
```json
{
  "job_id": "...",
  "status": "processing",
  "message": "Job is still processing",
  "created_at": "..."
}
```

### Step 2: Check Render Logs
Look for the job ID in logs:
```
[API] Starting renovation estimation for /tmp/async_estimate_YOUR_JOB_ID
```

### Step 3: Check Result
```bash
curl https://estimator-bb7k.onrender.com/result/YOUR_JOB_ID
```

Expected response (when complete):
```json
{
  "status": "success",
  "message": "Estimation completed successfully",
  "files": {
    "excel_file": "filename.xlsx"
  },
  "download_urls": {
    "excel_file": "/download/filename.xlsx"
  }
}
```

## Performance Expectations

| Transcript Size | Expected Time | Max Time |
|----------------|---------------|----------|
| < 10KB | 30-60 seconds | 2 minutes |
| 10-50KB | 1-3 minutes | 5 minutes |
| 50-100KB | 3-5 minutes | 10 minutes |
| > 100KB | 5-10 minutes | 15 minutes |

## Getting Help

If you're stuck:

1. **Check Render Logs** - Most issues show up here
2. **Check Power Automate Run History** - See what the API returned
3. **Test with curl** - Isolate if it's a Power Automate issue
4. **Check this guide** - Common issues are documented above

## Test Command

Test your API directly:
```bash
# Create test transcript
cat > test.txt << 'EOF'
Speaker 1: We need to renovate the kitchen.
Speaker 2: I recommend new cabinets and countertops.
The kitchen is about 200 square feet.
EOF

# Encode to base64
TRANSCRIPT_BASE64=$(base64 -i test.txt)

# Test API
curl -X POST https://estimator-bb7k.onrender.com/estimate_async \
  -H "Content-Type: application/json" \
  -d "{
    \"transcript_base64\": \"$TRANSCRIPT_BASE64\",
    \"polycam_url\": \"YOUR_POLYCAM_URL\"
  }"

# Get job ID from response, then check status
curl https://estimator-bb7k.onrender.com/status/JOB_ID
```

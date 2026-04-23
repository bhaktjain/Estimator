# Power Automate Fix - Correct Body Format

## ❌ Current Issue

Your HTTP body has:
```json
{
  "transcript_text": "...",
  "polycam_base64": "..."
}
```

But the API expects:
```json
{
  "transcript_base64": "...",
  "polycam_base64": "..."
}
```

## ✅ Solution

Change `transcript_text` to `transcript_base64`

## Correct Power Automate HTTP Action Setup

### Method
```
POST
```

### URI
```
https://estimator-bb7k.onrender.com/estimate_async
```

### Headers
```json
{
  "Content-Type": "application/json"
}
```

### Body (Option 1 - If you have transcript text content)
```json
{
  "transcript_base64": "@{base64(body('Get_transcript_content'))}",
  "polycam_base64": "@{base64(body('Get_polycam_content'))}",
  "response_mode": "json"
}
```

### Body (Option 2 - If you have transcript URL)
```json
{
  "transcript_url": "@{outputs('Get_transcript_URL')}",
  "polycam_url": "@{outputs('Get_polycam_URL')}",
  "response_mode": "json"
}
```

### Body (Option 3 - Mix of base64 and URL)
```json
{
  "transcript_base64": "@{base64(body('Get_transcript_content'))}",
  "polycam_url": "@{outputs('Get_polycam_URL')}",
  "response_mode": "json"
}
```

## Complete Example for Power Automate

### Step 1: Get File Content
Action: **Get file content**
- File: Your transcript.txt file
- Output: File content

### Step 2: HTTP Request
Action: **HTTP**
- Method: `POST`
- URI: `https://estimator-bb7k.onrender.com/estimate_async`
- Headers:
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- Body:
  ```json
  {
    "transcript_base64": "@{base64(body('Get_file_content'))}",
    "polycam_url": "YOUR_POLYCAM_URL_HERE",
    "response_mode": "json"
  }
  ```

### Step 3: Parse JSON
Action: **Parse JSON**
- Content: `@{body('HTTP')}`
- Schema:
  ```json
  {
    "type": "object",
    "properties": {
      "status": {"type": "string"},
      "job_id": {"type": "string"},
      "message": {"type": "string"}
    }
  }
  ```

### Step 4: Wait for Job (Delay)
Action: **Delay**
- Duration: 2 minutes

### Step 5: Get Result
Action: **HTTP**
- Method: `GET`
- URI: `https://estimator-bb7k.onrender.com/result/@{body('Parse_JSON')?['job_id']}`

## Quick Fix for Your Current Flow

In your HTTP action body, change this line:
```
"transcript_text": "Conference Room (Ravit Doozli) – Speaker 2: Hi, g..."
```

To:
```
"transcript_base64": "@{base64('Conference Room (Ravit Doozli) – Speaker 2: Hi, g...')}"
```

Or better yet, if you're getting this from a file:
```
"transcript_base64": "@{base64(body('Get_file_content'))}"
```

## API Parameter Names Reference

| What You Have | What API Expects | Type |
|---------------|------------------|------|
| transcript_text | transcript_base64 | base64 string |
| transcript_text | transcript_url | URL string |
| transcript_text | transcript_json | JSON object |
| polycam_base64 | polycam_base64 | ✅ Correct |
| polycam_url | polycam_url | ✅ Correct |

## Test Your Fix

After making the change, your request should look like:
```json
{
  "transcript_base64": "Q29uZmVyZW5jZSBSb29tIC...",
  "polycam_base64": "JVBERi0xLjQKJeLjz9MKMy...",
  "response_mode": "json"
}
```

And you should get a response like:
```json
{
  "status": "queued",
  "job_id": "abc-123-def-456",
  "message": "Estimation job queued successfully"
}
```

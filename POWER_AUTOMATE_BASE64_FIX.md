# Power Automate Base64 Fix

## The Problem

The API expects `transcript_base64` to be a **base64-encoded string**, but Power Automate might be sending the raw text.

## Solution Options

### Option 1: Use base64() Function in Power Automate (RECOMMENDED)

In your HTTP action body:

```json
{
  "transcript_base64": "@{base64(body('Get_file_content'))}",
  "polycam_base64": "@{base64(body('Get_polycam_content'))}",
  "response_mode": "json"
}
```

**Important:** Make sure you're using `body('Get_file_content')` not `body('Get_file_content')?['$content']`

### Option 2: If You Already Have Base64 Content

If your file content is already in base64 format (like from SharePoint), use:

```json
{
  "transcript_base64": "@{body('Get_file_content')?['$content']}",
  "polycam_base64": "@{body('Get_polycam_content')?['$content']}",
  "response_mode": "json"
}
```

### Option 3: Use URL Instead (EASIEST)

If your files are accessible via URL, this is the simplest:

```json
{
  "transcript_url": "https://your-sharepoint-url/transcript.txt",
  "polycam_url": "https://your-sharepoint-url/polycam.pdf",
  "response_mode": "json"
}
```

## Complete Power Automate Flow

### Step 1: Get File Content
- Action: **Get file content**
- Site Address: Your SharePoint site
- File Identifier: Your transcript.txt file

### Step 2: Compose Base64 (Optional - for debugging)
- Action: **Compose**
- Inputs: `@{base64(body('Get_file_content'))}`
- This lets you see the base64 string

### Step 3: HTTP Request
- Action: **HTTP**
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
    "polycam_url": "YOUR_POLYCAM_URL",
    "response_mode": "json"
  }
  ```

## Common Issues

### Issue 1: "Invalid transcript_base64"
**Cause:** The base64 string is malformed or not properly encoded

**Fix:** Make sure you're using the `base64()` function:
```
@{base64(body('Get_file_content'))}
```

NOT just:
```
@{body('Get_file_content')}
```

### Issue 2: Content is already base64
**Cause:** SharePoint/OneDrive returns content in base64 format with `$content` property

**Fix:** Use:
```
@{body('Get_file_content')?['$content']}
```

### Issue 3: Special characters in transcript
**Cause:** Non-UTF-8 characters in the file

**Fix:** Ensure your transcript.txt file is saved as UTF-8 encoding

## Test Your Base64 Encoding

To verify your base64 is correct, you can test it:

1. In Power Automate, add a **Compose** action after getting file content:
   ```
   @{base64(body('Get_file_content'))}
   ```

2. Run the flow and copy the output

3. Test it with this command:
   ```bash
   echo "YOUR_BASE64_STRING" | base64 -d
   ```
   
   You should see your transcript text.

## Working Example

Here's a complete working body for Power Automate:

```json
{
  "transcript_base64": "@{base64(body('Get_file_content'))}",
  "polycam_base64": "@{base64(body('Get_file_content_2'))}",
  "api_key": "YOUR_API_KEY_IF_NEEDED",
  "max_tokens": 10000,
  "response_mode": "json"
}
```

## Alternative: Use Direct File Upload

Instead of `/estimate_async`, you can use `/estimate_files` endpoint which accepts actual files:

**This is NOT supported via JSON body** - you'd need to use multipart/form-data which is harder in Power Automate.

Stick with the base64 approach above.

## Debugging Steps

1. **Check if base64 is being applied:**
   - Add a Compose action with: `@{base64('test')}`
   - Should output: `dGVzdA==`

2. **Check your file content:**
   - Add a Compose action with: `@{body('Get_file_content')}`
   - Make sure it's the actual text content

3. **Check the encoded result:**
   - Add a Compose action with: `@{base64(body('Get_file_content'))}`
   - Should be a long string of letters/numbers

4. **Test with a simple transcript:**
   - Create a test file with just: "Test transcript"
   - Base64 should be: `VGVzdCB0cmFuc2NyaXB0`

## Still Having Issues?

If you're still getting "Invalid transcript_base64", share:
1. The exact Power Automate expression you're using
2. A sample of what the base64 string looks like (first 50 characters)
3. Whether you're getting the file from SharePoint, OneDrive, or elsewhere

# Quick Reference - TXT Transcript Support

## ✅ What's New
Your renovation estimation API now accepts **transcript.txt** files!

## 📝 Supported Formats
- `.txt` - Plain text transcripts (NEW!)
- `.json` - JSON transcripts
- `.pdf` - PDF transcripts

## 🚀 Quick Start

### Upload a .txt file
```bash
curl -X POST https://your-api.onrender.com/estimate \
  -F "transcript=@transcript.txt" \
  -F "polycam=@polycam.pdf"
```

### Use with base64
```bash
TRANSCRIPT=$(base64 -i transcript.txt)
curl -X POST https://your-api.onrender.com/estimate_json \
  -H "Content-Type: application/json" \
  -d "{\"transcript_base64\": \"$TRANSCRIPT\", \"polycam_url\": \"URL\"}"
```

### Local processing
```bash
python3 run_chunked_estimation.py \
  --transcript transcript.txt \
  --polycam polycam.pdf \
  --api_key YOUR_KEY
```

## 🧪 Test It
```bash
./test_full_pipeline.sh
```

## 📚 More Info
- **API Usage:** See `API_USAGE.md`
- **Deployment:** See `DEPLOYMENT_CHECKLIST.md`
- **Changes:** See `CHANGES_SUMMARY.md`

## ✨ Key Points
- ✅ Backward compatible - all existing code works
- ✅ Auto-detects JSON vs plain text
- ✅ Same API endpoints
- ✅ Same response format
- ✅ All tests passing

## 🔧 Troubleshooting

**Issue:** File not accepted
- **Solution:** Ensure file extension is .txt, .json, or .pdf

**Issue:** Processing fails
- **Solution:** Check file encoding is UTF-8

**Issue:** Empty output
- **Solution:** Verify transcript has actual content

## 📞 Health Check
```bash
curl https://your-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "renovation-estimation-api",
  "api_key_set": true
}
```

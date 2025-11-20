# Deployment Commands

## Pre-Deployment Checklist

Run tests to verify everything works:
```bash
./test_full_pipeline.sh
```

Expected output: All tests pass ✅

## Deploy to Render

### Step 1: Commit Changes
```bash
git add .
git commit -m "Add support for transcript.txt files

- Updated process_transcript.py to handle .txt files
- Updated API endpoints to accept .txt transcripts
- Added comprehensive documentation and tests
- Backward compatible with existing PDF/JSON workflows"
```

### Step 2: Push to Deploy
```bash
git push origin main
```

Render will automatically deploy (auto-deploy is enabled in render.yaml).

### Step 3: Monitor Deployment
1. Go to https://dashboard.render.com
2. Select your service: `renovation-estimation-api`
3. Watch the deployment logs
4. Wait for "Deploy succeeded" message

### Step 4: Verify Deployment
```bash
# Health check
curl https://your-app.onrender.com/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "renovation-estimation-api",
#   "timestamp": "...",
#   "api_key_set": true
# }
```

### Step 5: Test with TXT File
```bash
# Create a test transcript
cat > test.txt << 'EOF'
Speaker 1: We need to renovate the kitchen.
Speaker 2: I recommend new cabinets and countertops.
EOF

# Test the API
curl -X POST https://your-app.onrender.com/estimate \
  -F "transcript=@test.txt" \
  -F "polycam=@polycam.pdf" \
  -F "response_mode=json"

# Clean up
rm test.txt
```

## Rollback (if needed)

If something goes wrong:
```bash
git revert HEAD
git push origin main
```

Render will automatically deploy the previous version.

## Environment Variables

Verify these are set in Render dashboard:
- `OPENAI_API_KEY` - Your OpenAI API key
- `PYTHON_VERSION` - 3.11.9
- `WEB_CONCURRENCY` - 1

## Troubleshooting

### Build fails
- Check requirements.txt has all dependencies
- Verify Python version is 3.11.9
- Check Render logs for specific error

### Deploy succeeds but API fails
- Check environment variables are set
- Verify OPENAI_API_KEY is valid
- Check /health endpoint response

### TXT files not accepted
- Verify deployment completed successfully
- Check API version with /health endpoint
- Review Render logs for errors

## Post-Deployment

1. Update Power Automate flows (if needed)
2. Notify team of new .txt support
3. Update any documentation/wikis
4. Monitor logs for any issues

## Quick Commands

```bash
# View recent logs
render logs --tail

# Restart service
render restart

# Check service status
render status
```

## Success Criteria

✅ Health check returns "healthy"
✅ Can upload .txt files
✅ Can upload .json files (backward compatibility)
✅ Can upload .pdf files (backward compatibility)
✅ Excel output generated successfully
✅ No errors in logs

## Support

If you encounter issues:
1. Check Render logs
2. Run local tests: `./test_full_pipeline.sh`
3. Review `TROUBLESHOOTING.md` (if available)
4. Check `API_USAGE.md` for correct usage

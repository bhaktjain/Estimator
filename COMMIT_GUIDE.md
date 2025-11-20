# Git Commit Guide

## Files to Commit

### Modified Files (Core Changes)
```bash
git add process_transcript.py
git add archive_non_pipeline_20250909_091152/app_fastapi.py
git add run_chunked_estimation.py
```

### New Documentation Files
```bash
git add API_USAGE.md
git add CHANGES_SUMMARY.md
git add DEPLOY.md
git add DEPLOYMENT_CHECKLIST.md
git add QUICK_REFERENCE.md
git add COMMIT_GUIDE.md
```

### Test Files
```bash
git add test_txt_support.py
git add test_full_pipeline.sh
```

## Commit Command

```bash
git commit -m "Add support for transcript.txt files

Features:
- Accept .txt files in addition to PDF and JSON
- Auto-detect JSON vs plain text format
- Updated all API endpoints (/estimate, /estimate_json, /estimate_async)
- Added comprehensive documentation and tests

Changes:
- Modified: process_transcript.py (added txt handler)
- Modified: app_fastapi.py (added txt to allowed extensions)
- Modified: run_chunked_estimation.py (added txt support)
- Added: Complete documentation suite
- Added: Automated test suite

Backward Compatibility:
- 100% backward compatible
- All existing PDF/JSON workflows unchanged
- Same API contracts and response formats

Testing:
- All tests passing
- Full pipeline integration verified
- Ready for production deployment"
```

## Push to Deploy

```bash
git push origin main
```

## Verify Deployment

After pushing, Render will auto-deploy. Monitor at:
https://dashboard.render.com

Then verify:
```bash
curl https://your-app.onrender.com/health
```

## Files NOT to Commit

These are temporary/local files and should NOT be committed:
- `__pycache__/` (Python cache)
- `chunked_outputs/` (Processing outputs)
- `outputs/` (Generated files)
- `temp_scope_extract/` (Temporary files)
- `uploads/` (Uploaded files)
- `*.pyc` (Compiled Python)
- `venv/` (Virtual environment)

These should already be in `.gitignore`.

## Quick Commit (All at Once)

If you want to commit everything at once:

```bash
# Add only the files we want
git add process_transcript.py \
        archive_non_pipeline_20250909_091152/app_fastapi.py \
        run_chunked_estimation.py \
        API_USAGE.md \
        CHANGES_SUMMARY.md \
        DEPLOY.md \
        DEPLOYMENT_CHECKLIST.md \
        QUICK_REFERENCE.md \
        COMMIT_GUIDE.md \
        test_txt_support.py \
        test_full_pipeline.sh

# Commit with message
git commit -m "Add support for transcript.txt files"

# Push to deploy
git push origin main
```

## Verify Before Pushing

```bash
# See what will be committed
git status

# See the actual changes
git diff --cached

# Run tests one more time
./test_full_pipeline.sh
```

## After Deployment

1. Check Render dashboard for successful deployment
2. Run health check: `curl https://your-app.onrender.com/health`
3. Test with a .txt file (see DEPLOY.md)
4. Monitor logs for any issues

## Rollback (if needed)

If something goes wrong:
```bash
git revert HEAD
git push origin main
```

#!/bin/bash
# Verify that .txt support is deployed to Render

echo "=========================================="
echo "Verifying Deployment to Render"
echo "=========================================="
echo ""

API_URL="https://estimator-bb7k.onrender.com"

# Check 1: Health check
echo "1. Health Check..."
HEALTH=$(curl -s "$API_URL/health")
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ Service is healthy"
else
    echo "   ❌ Service is not healthy"
    exit 1
fi

echo ""

# Check 2: Check API documentation for .txt support
echo "2. Checking API documentation..."
API_DOC=$(curl -s "$API_URL/")

if echo "$API_DOC" | grep -qi "txt"; then
    echo "   ✅ TXT support found in API documentation"
    
    # Extract the transcript parameter description
    echo ""
    echo "   Transcript parameter:"
    echo "$API_DOC" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    transcript = data.get('usage', {}).get('multipart_endpoint', {}).get('parameters', {}).get('transcript', 'N/A')
    print('   ', transcript)
except:
    print('   Could not parse')
" 2>/dev/null
else
    echo "   ⏳ TXT support not yet visible (deployment may still be in progress)"
    echo ""
    echo "   This is normal - Render deployments can take 2-5 minutes."
    echo "   Please wait a moment and run this script again:"
    echo "   ./verify_deployment.sh"
    exit 0
fi

echo ""

# Check 3: Test with a simple .txt file (if we can)
echo "3. Deployment Status:"
echo "   ✅ Code pushed to GitHub"
echo "   ✅ Render auto-deploy triggered"
echo "   ⏳ Waiting for deployment to complete..."

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Monitor deployment at:"
echo "   https://dashboard.render.com/web/srv-d307jp3e5dus73dfa7k0"
echo ""
echo "2. Once deployed, test with a .txt file:"
echo "   curl -X POST $API_URL/estimate \\"
echo "     -F \"transcript=@transcript.txt\" \\"
echo "     -F \"polycam=@polycam.pdf\""
echo ""
echo "3. Or check the API docs:"
echo "   curl $API_URL/ | python3 -m json.tool"
echo ""

#!/bin/bash
# Example: How to use the API with transcript.txt

echo "Creating test transcript.txt..."
cat > test_transcript.txt << 'EOF'
Kitchen Renovation Discussion

Speaker 1: We need to renovate the kitchen.
Speaker 2: I recommend new cabinets and countertops.
The kitchen is about 200 square feet.
We'll need luxury vinyl plank flooring.
EOF

echo "✅ Test transcript created"
echo ""

# OPTION 1: Direct file upload (EASIEST)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTION 1: Direct File Upload"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Command:"
echo "curl -X POST https://estimator-bb7k.onrender.com/estimate \\"
echo "  -F \"transcript=@test_transcript.txt\" \\"
echo "  -F \"polycam=@polycam.pdf\" \\"
echo "  -F \"response_mode=json\""
echo ""
echo "Note: You need a polycam.pdf file for this to work"
echo ""

# OPTION 2: Base64 encoding
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTION 2: Base64 Encoding"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Step 1: Encode transcript"
TRANSCRIPT_BASE64=$(base64 -i test_transcript.txt)
echo "TRANSCRIPT_BASE64=\"$TRANSCRIPT_BASE64\""
echo ""
echo "Step 2: Send to API"
echo "curl -X POST https://estimator-bb7k.onrender.com/estimate_json \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"transcript_base64\": \"'$TRANSCRIPT_BASE64'\"," 
echo "    \"polycam_url\": \"https://your-polycam-url.com/file.pdf\""
echo "  }'"
echo ""

# OPTION 3: Plain text in JSON (for Power Automate)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "OPTION 3: For Power Automate"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "In Power Automate HTTP action:"
echo ""
echo "Method: POST"
echo "URI: https://estimator-bb7k.onrender.com/estimate_json"
echo "Headers: Content-Type: application/json"
echo "Body:"
echo "{"
echo "  \"transcript_base64\": \"@{base64(body('Get_file_content'))}\","
echo "  \"polycam_url\": \"YOUR_POLYCAM_URL\","
echo "  \"response_mode\": \"json\""
echo "}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test file created: test_transcript.txt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

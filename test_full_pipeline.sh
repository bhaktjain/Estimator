#!/bin/bash
# Full pipeline test for .txt transcript support

set -e  # Exit on error

echo "=========================================="
echo "Full Pipeline Test - TXT Transcript"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create test transcript
echo -e "\n${GREEN}[1/5]${NC} Creating test transcript.txt..."
cat > test_transcript.txt << 'EOF'
Kitchen Renovation Discussion

Speaker 1: Let's discuss the kitchen renovation project.

Speaker 2: Based on my assessment, here's what we need:

1. Flooring: Remove old tile and install new luxury vinyl plank. The kitchen is 250 square feet.

2. Cabinets: Replace all upper and lower cabinets. We have 15 linear feet of uppers and 20 linear feet of lowers.

3. Countertops: Install quartz countertops. Total of 35 square feet needed.

4. Backsplash: Ceramic tile backsplash, approximately 40 square feet.

5. Appliances: Not included in renovation scope.

6. Painting: Fresh paint on walls and ceiling after cabinet installation.

Speaker 1: What about electrical work?

Speaker 2: We'll need to add two new outlets and upgrade the lighting. I recommend recessed LED lights - about 6 fixtures.

Speaker 1: Timeline?

Speaker 2: Approximately 3 weeks for complete renovation.
EOF

echo "✅ Test transcript created"

# Test 1: Process transcript
echo -e "\n${GREEN}[2/5]${NC} Testing process_transcript.py..."
python3 process_transcript.py test_transcript.txt --output_dir test_output --max_tokens 1000

if [ -d "test_output" ] && [ "$(ls -A test_output)" ]; then
    echo "✅ Transcript processed successfully"
    echo "   Chunks created: $(ls test_output/*.txt | wc -l)"
else
    echo -e "${RED}❌ Failed to process transcript${NC}"
    exit 1
fi

# Test 2: Verify chunk content
echo -e "\n${GREEN}[3/5]${NC} Verifying chunk content..."
if grep -q "kitchen" test_output/chunk_1.txt; then
    echo "✅ Chunk content verified"
else
    echo -e "${RED}❌ Chunk content verification failed${NC}"
    exit 1
fi

# Test 3: Check API configuration
echo -e "\n${GREEN}[4/5]${NC} Checking API configuration..."
python3 -c "
import sys
sys.path.insert(0, 'archive_non_pipeline_20250909_091152')
from app_fastapi import ALLOWED_EXTENSIONS
assert 'txt' in ALLOWED_EXTENSIONS, 'txt not in ALLOWED_EXTENSIONS'
print('✅ API configured to accept .txt files')
"

# Test 4: Run comprehensive test
echo -e "\n${GREEN}[5/5]${NC} Running comprehensive test suite..."
python3 test_txt_support.py

# Cleanup
echo -e "\n${GREEN}Cleaning up...${NC}"
rm -rf test_transcript.txt test_output

echo -e "\n=========================================="
echo -e "${GREEN}✅ All tests passed!${NC}"
echo "=========================================="
echo ""
echo "The system is ready to accept .txt transcripts."
echo ""
echo "Next steps:"
echo "1. Commit changes: git add . && git commit -m 'Add .txt transcript support'"
echo "2. Push to deploy: git push origin main"
echo "3. Verify on Render: curl https://your-app.onrender.com/health"
echo ""

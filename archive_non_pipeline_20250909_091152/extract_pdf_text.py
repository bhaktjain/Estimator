#!/usr/bin/env python3
"""
Extract full text from a PDF file without chunking.
"""

import argparse
import pdfplumber
import sys
from pathlib import Path

def extract_pdf_text(pdf_path, output_file=None):
    """Extract all text from PDF and optionally save to file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    all_text.append(f"--- Page {page_num} ---\n{text}")
            
            full_text = '\n\n'.join(all_text)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_text)
                print(f"[SUCCESS] Extracted text saved to: {output_file}")
            else:
                print(full_text)
                
            return full_text
            
    except Exception as e:
        print(f"[ERROR] Failed to extract text from {pdf_path}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Extract full text from PDF without chunking")
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('--output_file', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_file).exists():
        print(f"[ERROR] PDF file not found: {args.pdf_file}")
        sys.exit(1)
    
    extract_pdf_text(args.pdf_file, args.output_file)

if __name__ == "__main__":
    main() 
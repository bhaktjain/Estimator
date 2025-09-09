"""
send_files_to_chatgpt_text.py

Send three main project files and a prompt to OpenAI's Chat Completions API (gpt-4o), 
by extracting text content from PDFs and sending as text.

Usage:
  python send_files_to_chatgpt_text.py --file1 file1.pdf --file2 file2.pdf --file3 file3.txt --prompt "Summarize the key points." [--sample_scope sample1.csv --sample_scope sample2.csv ...] [--api_key YOUR_API_KEY]

Supported file types: PDF, DOCX, TXT for uploads; CSVs are appended as markdown tables in the prompt.
"""
import argparse
import os
import openai
from pathlib import Path
import csv

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
    except ImportError:
        print("[WARNING] pdfplumber not available, using fallback text extraction")
        return f"[PDF content from {pdf_path} - text extraction not available]"
    except Exception as e:
        print(f"[WARNING] Failed to extract text from {pdf_path}: {e}")
        return f"[PDF content from {pdf_path} - extraction failed: {e}]"

def csv_to_markdown_table(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        if not reader:
            return ''
        header = reader[0]
        rows = reader[1:]
        md = '| ' + ' | '.join(header) + ' |\n'
        md += '| ' + ' | '.join(['---'] * len(header)) + ' |\n'
        for row in rows:
            md += '| ' + ' | '.join(row) + ' |\n'
        return md

def main():
    parser = argparse.ArgumentParser(description="Send 3 files and a prompt to OpenAI Chat Completions API (gpt-4o), by extracting text content.")
    parser.add_argument("--file1", required=True, help="First file (PDF, DOCX, or TXT)")
    parser.add_argument("--file2", required=True, help="Second file (PDF, DOCX, or TXT)")
    parser.add_argument("--file3", required=True, help="Third file (PDF, DOCX, or TXT)")
    parser.add_argument("--prompt", required=True, help="Prompt to send to ChatGPT")
    parser.add_argument("--sample_scope", action='append', default=[], help="Sample scope CSV file (can be used multiple times)")
    parser.add_argument("--api_key", required=False, help="OpenAI API key (optional, will use env if not provided)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key must be provided via --api_key or OPENAI_API_KEY environment variable.")

    client = openai.OpenAI(api_key=api_key)
    
    # Extract text content from all files
    file_contents = []
    file_names = []
    
    for i, path in enumerate([args.file1, args.file2, args.file3]):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        print(f"[INFO] Processing file {i+1}: {path}")
        ext = Path(path).suffix.lower()
        
        if ext == '.pdf':
            # Extract text from PDF
            text_content = extract_text_from_pdf(path)
            file_contents.append(text_content)
            file_names.append(f"File {i+1} ({Path(path).name})")
            print(f"[SUCCESS] Extracted {len(text_content)} characters from {path}")
        elif ext == '.txt':
            # Read text file directly
            with open(path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            file_contents.append(text_content)
            file_names.append(f"File {i+1} ({Path(path).name})")
            print(f"[SUCCESS] Read {len(text_content)} characters from {path}")
        else:
            print(f"[WARNING] Unsupported file type: {path}, skipping")
            file_contents.append(f"[Unsupported file: {path}]")
            file_names.append(f"File {i+1} ({Path(path).name})")

    prompt = args.prompt
    # Append section_minimums_margins.csv as markdown table to the prompt
    cheatsheet_csv = "section_minimums_margins.csv"
    if os.path.exists(cheatsheet_csv):
        md_table = csv_to_markdown_table(cheatsheet_csv)
        prompt += f"\n\nSection Markup and Minimums Cheatsheet ({cheatsheet_csv}):\n" + md_table

    # Append all sample scope CSVs as markdown tables to the prompt
    for i, csv_path in enumerate(args.sample_scope, 1):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Sample scope file not found: {csv_path}")
        md_table = csv_to_markdown_table(csv_path)
        prompt += f"\n\nSample Scope Table {i} ({Path(csv_path).name}):\n" + md_table

    # Build the complete prompt with file contents
    complete_prompt = prompt + "\n\n"
    for i, (content, name) in enumerate(zip(file_contents, file_names)):
        complete_prompt += f"=== {name} ===\n{content}\n\n"

    # Add strict guardrails so the model never refuses and always returns results
    # Detect if Polycam text is likely missing/failed
    polycam_text = file_contents[1] if len(file_contents) >= 2 else ""
    polycam_unavailable = (
        isinstance(polycam_text, str)
        and ("extraction failed" in polycam_text.lower() or "text extraction not available" in polycam_text.lower())
    ) or (isinstance(polycam_text, str) and len(polycam_text.strip()) < 50)

    system_guardrails = (
        "You are a professional renovation estimator. \n"
        "CRITICAL RULES: \n"
        "- Never refuse or defer. Always produce a full estimate. \n"
        "- If any source is missing/unreadable (e.g., Polycam), proceed using reasonable assumptions based on the master pricing sheet and transcript. \n"
        "- Explicitly mark assumptions in descriptions but provide concrete numeric quantities and subtotals. \n"
        "- Apply markups exactly as instructed. \n"
        "- Output must be a single JSON object wrapped in a ```json code block, with the exact schema requested. No prose before/after the block. \n"
    )

    if polycam_unavailable:
        system_guardrails += (
            "- Polycam measurements unavailable: infer room areas and linear feet using standard residential assumptions (e.g., kitchen counter depth ~2.5 ft, small bath tile ~60-80 SF) and clearly tag them as assumed.\n"
        )

    # Use Chat Completions API
    print("[INFO] Sending request to OpenAI Chat Completions API...")
    print(f"[INFO] Total prompt length: {len(complete_prompt)} characters")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_guardrails
                },
                {
                    "role": "user",
                    "content": complete_prompt
                }
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        # Extract and print the response
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content
            print("[RESPONSE]")
            print(content)
            
            # Write to file
            with open("estimate_output.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("[SUCCESS] Response saved to estimate_output.txt")
        else:
            print("[ERROR] No response received")
            
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return
    
    print("[SUCCESS] Processing complete!")

if __name__ == "__main__":
    main()

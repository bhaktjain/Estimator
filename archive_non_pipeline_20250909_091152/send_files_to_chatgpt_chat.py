"""
send_files_to_chatgpt_chat.py

Send three main project files and a prompt to OpenAI's Chat Completions API (gpt-4o), 
which can handle large files better than the Responses API.

Usage:
  python send_files_to_chatgpt_chat.py --file1 file1.pdf --file2 file2.pdf --file3 file3.txt --prompt "Summarize the key points." [--sample_scope sample1.csv --sample_scope sample2.csv ...] [--api_key sk-proj-...]

Supported file types: PDF, DOCX, TXT for uploads; CSVs are appended as markdown tables in the prompt.
"""
import argparse
import os
import openai
from pathlib import Path
import csv

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
    parser = argparse.ArgumentParser(description="Send 3 files and a prompt to OpenAI Chat Completions API (gpt-4o), which handles large files better.")
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
    
    # Upload all files to OpenAI
    file_ids = []
    file_names = []
    
    for i, path in enumerate([args.file1, args.file2, args.file3]):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        print(f"[INFO] Uploading file {i+1}: {path}")
        try:
            with open(path, "rb") as f:
                file_obj = client.files.create(file=f, purpose="assistants")
                file_ids.append(file_obj.id)
                file_names.append(f"File {i+1} ({Path(path).name})")
                print(f"[SUCCESS] Uploaded {path} as file ID: {file_obj.id}")
        except Exception as e:
            print(f"[ERROR] Failed to upload {path}: {e}")
            return

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

    # Use Chat Completions API with file attachments
    print("[INFO] Sending request to OpenAI Chat Completions API...")
    
    # Prepare the message with file attachments
    message_content = [
        {"type": "text", "text": prompt}
    ]
    
    # Add file attachments
    for file_id in file_ids:
        message_content.append({
            "type": "file",
            "file_id": file_id
        })
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": message_content
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
    
    # Clean up uploaded files
    print("[INFO] Cleaning up uploaded files...")
    for file_id in file_ids:
        try:
            client.files.delete(file_id)
            print(f"[INFO] Deleted file: {file_id}")
        except Exception as e:
            print(f"[WARNING] Failed to delete file {file_id}: {e}")
    
    print("[SUCCESS] Processing complete!")

if __name__ == "__main__":
    main()


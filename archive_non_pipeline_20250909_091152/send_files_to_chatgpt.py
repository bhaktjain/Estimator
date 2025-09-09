"""
send_files_to_chatgpt.py

Send three main project files and a prompt to OpenAI's Responses API (gpt-4o), with any number of sample scope CSVs appended as markdown tables to the prompt. Prints the model's reply.

Usage:
  python send_files_to_chatgpt.py --file1 file1.pdf --file2 file2.docx --file3 file3.txt --prompt "Summarize the key points." [--sample_scope sample1.csv --sample_scope sample2.csv ...] [--api_key sk-proj-...]

Supported file types: PDF, DOCX, TXT for uploads; CSVs are appended as markdown tables in the prompt.
"""
import argparse
import os
import openai
from pathlib import Path
import csv
import time

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
    parser = argparse.ArgumentParser(description="Send 3 files and a prompt to OpenAI Assistants API (gpt-4o), with any number of sample scope CSVs appended as markdown tables to the prompt.")
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
    
    # Upload all files to OpenAI (this handles large files better)
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

    # Create an assistant with the files
    print("[INFO] Creating OpenAI assistant...")
    assistant = client.beta.assistants.create(
        name="Renovation Estimator",
        instructions=prompt,
        model="gpt-4o",
        tools=[{"type": "file_search"}]
    )
    
    # Add files to the assistant
    print("[INFO] Adding files to assistant...")
    for file_id in file_ids:
        client.beta.assistants.files.create(
            assistant_id=assistant.id,
            file_id=file_id
        )
    
    # Create a thread
    print("[INFO] Creating conversation thread...")
    thread = client.beta.threads.create()
    
    # Add the prompt as a message
    print("[INFO] Sending prompt to assistant...")
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    # Run the assistant
    print("[INFO] Running assistant...")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    # Wait for completion
    print("[INFO] Waiting for response...")
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break
        elif run_status.status == 'failed':
            print("[ERROR] Assistant run failed")
            return
        elif run_status.status == 'requires_action':
            print("[INFO] Assistant requires action, continuing...")
        time.sleep(2)
    
    # Get the response
    print("[INFO] Retrieving response...")
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    # Find the assistant's response
    output_lines = []
    for msg in messages.data:
        if msg.role == "assistant":
            for content in msg.content:
                if content.type == "text":
                    print(content.text.value)
                    output_lines.append(content.text.value)
    
    # Write to file
    with open("estimate_output.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(output_lines))
    
    # Clean up
    print("[INFO] Cleaning up...")
    client.beta.assistants.delete(assistant.id)
    print("[SUCCESS] Processing complete!")

if __name__ == "__main__":
    main() 
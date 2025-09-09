#!/usr/bin/env python3
"""
regenerate_chunks.py

Regenerate all chunk outputs using the new text-based approach.
"""

import os
import subprocess
import sys

def main():
    # Directory containing the chunks - use current directory
    chunk_dir = "."
    
    if not os.path.exists(chunk_dir):
        print(f"Directory {chunk_dir} not found")
        return
    
    # Files to use
    master_pricing = "../../Master Pricing Sheet - Q1 - 2025 (2).pdf"
    polycam = "../../Polycam2.pdf"
    prompt_file = "../../estimation_prompt.txt"
    
    # Check if files exist
    for file in [master_pricing, polycam, prompt_file]:
        if not os.path.exists(file):
            print(f"Required file {file} not found")
            return
    
    # Read the prompt
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read()
    
    # Process each chunk
    for i in range(1, 6):
        chunk_file = f"transcript_chunks/chunk_{i}.txt"
        output_file = f"estimate_output_chunk_{i}.txt"
        
        if not os.path.exists(chunk_file):
            print(f"Chunk file {chunk_file} not found, skipping")
            continue
        
        print(f"Processing chunk {i}...")
        
        # Run the text-based script
        cmd = [
            "python3", "../../send_files_to_chatgpt_text.py",
            "--file1", master_pricing,
            "--file2", polycam,
            "--file3", chunk_file,
            "--prompt", prompt
        ]
        
        try:
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Move the output file to the correct location
            if os.path.exists("estimate_output.txt"):
                os.rename("estimate_output.txt", output_file)
                print(f"✅ Chunk {i} processed successfully")
            else:
                print(f"❌ No output file generated for chunk {i}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error processing chunk {i}: {e}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
        except Exception as e:
            print(f"❌ Unexpected error processing chunk {i}: {e}")
    
    print("Chunk regeneration complete!")

if __name__ == "__main__":
    main()

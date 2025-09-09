#!/usr/bin/env python3
"""
Process takeoff content and create chunks for estimation pipeline
"""
import os
import argparse
import tiktoken

def count_tokens(text, model="gpt-4o"):
    """Count tokens using tiktoken"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback: rough estimate (1 token ≈ 4 characters)
        return len(text) // 4

def split_by_tokens(text, max_tokens=1500, overlap_tokens=150):
    """Split text into chunks with overlap for better context"""
    chunks = []
    current_pos = 0
    
    while current_pos < len(text):
        # Find the end position for this chunk
        end_pos = min(current_pos + max_tokens * 4, len(text))  # Rough estimate
        
        # Try to find a good break point (sentence end, line break, etc.)
        if end_pos < len(text):
            # Look for sentence endings
            for i in range(end_pos, max(current_pos, end_pos - 200), -1):
                if text[i] in '.!?':
                    end_pos = i + 1
                    break
            
            # If no sentence ending, look for line breaks
            if end_pos == min(current_pos + max_tokens * 4, len(text)):
                for i in range(end_pos, max(current_pos, end_pos - 100), -1):
                    if text[i] == '\n':
                        end_pos = i + 1
                        break
        
        # Extract the chunk
        chunk = text[current_pos:end_pos].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move to next position with overlap
        if current_pos <= end_pos - (overlap_tokens * 4):
            current_pos = end_pos
        else:
            current_pos = end_pos
    
    return chunks

def process_takeoff_file(input_file, output_dir, max_tokens):
    """Process takeoff file and create chunks"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the takeoff file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"[INFO] Read {len(content)} characters from {input_file}")
    print(f"[INFO] Token count: {count_tokens(content)}")
    
    # Split into chunks
    chunks = split_by_tokens(content, max_tokens)
    
    # Save chunks
    for i, chunk in enumerate(chunks):
        chunk_file = os.path.join(output_dir, f'chunk_{i+1}.txt')
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
    
    print(f"[INFO] Created {len(chunks)} chunks in {output_dir}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Process takeoff files and create chunks")
    parser.add_argument("input_file", help="Path to takeoff file")
    parser.add_argument("--output_dir", required=True, help="Output directory for chunks")
    parser.add_argument("--max_tokens", type=int, default=1500, help="Max tokens per chunk")
    args = parser.parse_args()
    
    success = process_takeoff_file(args.input_file, args.output_dir, args.max_tokens)
    
    if success:
        print(f"[SUCCESS] Takeoff processed successfully. Output in: {args.output_dir}")
    else:
        print("[ERROR] Failed to process takeoff")
        exit(1)

if __name__ == "__main__":
    main()



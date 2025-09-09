#!/usr/bin/env python3
"""
Flexible Transcript Processor - Enhanced for Large Files
Handles both PDF and JSON transcript inputs with optimized chunking
"""
import json
import os
import argparse
from pathlib import Path
try:
    import tiktoken  # Optional
    _HAS_TIKTOKEN = True
except Exception:
    tiktoken = None
    _HAS_TIKTOKEN = False

def count_tokens(text, model="gpt-4o"):
    """Count tokens using tiktoken"""
    if _HAS_TIKTOKEN:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            pass
    # Fallback: rough estimate (1 token ≈ 4 characters)
    return len(text) // 4

def extract_text_from_json(json_data):
    """Extract meaningful text from JSON transcript data"""
    text_parts = []
    
    # Handle both array and object formats
    if isinstance(json_data, list) and len(json_data) > 0:
        # If it's an array, take the first item (should be the transcript data)
        json_data = json_data[0]
    
    # Extract summary if available
    if 'summary' in json_data and json_data['summary']:
        text_parts.append(f"SUMMARY: {json_data['summary']}")
    
    # Extract action items if available
    if 'action_items' in json_data and json_data['action_items']:
        action_text = "ACTION ITEMS: " + "; ".join([item.get('text', '') for item in json_data['action_items']])
        text_parts.append(action_text)
    
    # Extract key questions if available
    if 'key_questions' in json_data and json_data['key_questions']:
        questions_text = "KEY QUESTIONS: " + "; ".join([q.get('text', '') for q in json_data['key_questions']])
        text_parts.append(questions_text)
    
    # Extract topics if available
    if 'topics' in json_data and json_data['topics']:
        topics_text = "TOPICS: " + "; ".join([t.get('text', '') for t in json_data['topics']])
        text_parts.append(topics_text)
    
    # Extract chapter summaries if available
    if 'chapter_summaries' in json_data and json_data['chapter_summaries']:
        for i, chapter in enumerate(json_data['chapter_summaries']):
            chapter_text = f"CHAPTER {i+1}: {chapter.get('title', '')} - {chapter.get('description', '')}"
            if chapter.get('topics'):
                chapter_text += f" Topics: {', '.join(chapter['topics'])}"
            text_parts.append(chapter_text)
    
    # Extract transcript content if available (most important)
    if 'transcript' in json_data and 'speaker_blocks' in json_data['transcript']:
        speaker_blocks = json_data['transcript']['speaker_blocks']
        
        # For very long transcripts, sample key sections
        if len(speaker_blocks) > 100:
            # Take first 20%, middle 60%, and last 20% for better coverage
            first_count = max(10, len(speaker_blocks) // 5)
            middle_start = len(speaker_blocks) // 4
            middle_end = 3 * len(speaker_blocks) // 4
            last_count = max(10, len(speaker_blocks) // 5)
            
            # Sample from different sections
            sampled_blocks = (
                speaker_blocks[:first_count] +
                speaker_blocks[middle_start:middle_start + 20] +
                speaker_blocks[middle_end:middle_end + 20] +
                speaker_blocks[-last_count:]
            )
        else:
            sampled_blocks = speaker_blocks
        
        # Extract text from sampled blocks
        transcript_text = []
        for block in sampled_blocks:
            speaker = block.get('speaker', {}).get('name', 'Unknown')
            words = block.get('words', '')
            if words.strip():
                transcript_text.append(f"{speaker}: {words}")
        
        if transcript_text:
            text_parts.append("TRANSCRIPT EXCERPT:\n" + "\n".join(transcript_text))
    
    # Combine all parts
    combined_text = "\n\n".join(text_parts)
    
    # If still too long, truncate intelligently
    if len(combined_text) > 50000:  # 50K character limit
        combined_text = combined_text[:50000] + "\n\n[Content truncated for processing]"
    
    return combined_text

def split_by_tokens(text, max_tokens=3000, overlap_tokens=300):
    """Split text into chunks with overlap for better context"""
    if not text.strip():
        return []
    
    # Count total tokens
    total_tokens = count_tokens(text)
    
    # If text is small enough, return as single chunk
    if total_tokens <= max_tokens:
        return [text]
    
    # Split into chunks with overlap
    chunks = []
    current_pos = 0
    
    while current_pos < len(text):
        # Find the end position for this chunk
        end_pos = current_pos + (max_tokens * 4)  # Rough estimate
        
        if end_pos >= len(text):
            # Last chunk
            chunk_text = text[current_pos:]
        else:
            # Try to break at sentence boundary
            chunk_text = text[current_pos:end_pos]
            
            # Look for sentence endings to break cleanly
            sentence_endings = ['. ', '! ', '? ', '\n\n']
            for ending in sentence_endings:
                last_ending = chunk_text.rfind(ending)
                if last_ending > len(chunk_text) * 0.7:  # Only break if we're past 70% of chunk
                    chunk_text = chunk_text[:last_ending + len(ending)]
                    end_pos = current_pos + len(chunk_text)
                    break
        
        if chunk_text.strip():
            chunks.append(chunk_text.strip())
        
        # Move to next position with overlap
        current_pos = end_pos - (overlap_tokens * 4)  # Rough overlap estimate
        
        # Ensure we're making progress
        if current_pos <= end_pos - (overlap_tokens * 4):
            current_pos = end_pos
    
    return chunks

def process_pdf_transcript(pdf_path, output_dir, max_tokens):
    """Process PDF transcript"""
    try:
        import pdfplumber
        
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if not text.strip():
            print(f"[ERROR] No text extracted from PDF: {pdf_path}")
            return False
        
        # Split into chunks
        chunks = split_by_tokens(text, max_tokens)
        
        # Save chunks
        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(output_dir, f'chunk_{i+1}.txt')
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk)
        
        print(f"[INFO] Created {len(chunks)} chunks from PDF")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to process PDF: {e}")
        return False

def process_json_transcript(json_path, output_dir, max_tokens):
    """Process JSON transcript with enhanced text extraction"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract meaningful text using enhanced method
        text = extract_text_from_json(data)
        
        if not text.strip():
            print(f"[ERROR] No meaningful text extracted from JSON: {json_path}")
            return False
        
        print(f"[INFO] Extracted {len(text)} characters from JSON transcript")
        
        # Split into chunks
        chunks = split_by_tokens(text, max_tokens)
        
        # Save chunks
        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(output_dir, f'chunk_{i+1}.txt')
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk)
        
        print(f"[INFO] Created {len(chunks)} chunks from JSON")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to process JSON: {e}")
        return False

def process_transcript(input_path, output_dir, max_tokens):
    """Process transcript file (PDF or JSON)"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine file type and process accordingly
    if input_path.lower().endswith('.pdf'):
        return process_pdf_transcript(input_path, output_dir, max_tokens)
    elif input_path.lower().endswith('.json'):
        return process_json_transcript(input_path, output_dir, max_tokens)
    else:
        print(f"[ERROR] Unsupported file type: {input_path}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Process transcript files (PDF or JSON) with enhanced chunking")
    parser.add_argument("input_file", help="Path to transcript file (PDF or JSON)")
    parser.add_argument("--output_dir", required=True, help="Output directory for chunks")
    parser.add_argument("--max_tokens", type=int, default=3000, help="Max tokens per chunk")
    args = parser.parse_args()
    
    success = process_transcript(args.input_file, args.output_dir, args.max_tokens)
    
    if success:
        print(f"[SUCCESS] Transcript processed successfully. Output in: {args.output_dir}")
    else:
        print("[ERROR] Failed to process transcript")
        exit(1)

if __name__ == "__main__":
    main()

import pdfplumber
import re
import os
import argparse
import os
import re
from pathlib import Path
import pdfplumber

def count_tokens(text, encoding_name="cl100k_base"):
    try:
        import tiktoken
        enc = tiktoken.get_encoding(encoding_name)
        return len(enc.encode(text))
    except ImportError:
        print("[INFO] tiktoken not installed. Run: pip install tiktoken")
        return len(text.split())  # fallback: word count

def split_by_tokens(text, max_tokens, encoding_name="cl100k_base"):
    """Split text into chunks based on token count, ensuring no content is lost."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding(encoding_name)
    except ImportError:
        enc = None
    
    # If no tiktoken, fall back to character-based splitting
    if enc is None:
        print("[WARNING] tiktoken not available, using character-based splitting")
        char_limit = max_tokens * 4  # Rough estimate: 1 token ≈ 4 characters
        chunks = []
        for i in range(0, len(text), char_limit):
            chunk = text[i:i + char_limit]
            if chunk.strip():
                chunks.append(chunk)
        return chunks
    
    # Use tiktoken for accurate token counting
    chunks = []
    current_chunk = ""
    current_tokens = 0
    
    # Split by sentences first to avoid breaking mid-sentence
    sentences = text.split('. ')
    
    for sentence in sentences:
        # Add period back if it's not the last sentence
        if sentence != sentences[-1]:
            test_sentence = sentence + '. '
        else:
            test_sentence = sentence
        
        # Count tokens for this sentence
        sentence_tokens = len(enc.encode(test_sentence))
        
        # Check if adding this sentence would exceed the limit
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            # Start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = test_sentence
            current_tokens = sentence_tokens
        else:
            # Add to current chunk
            current_chunk += test_sentence
            current_tokens += sentence_tokens
    
    # Add the final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_text_by_section(pdf_path, output_dir, section_keywords=None, max_tokens=None):
    if section_keywords is None:
        section_keywords = [
            'kitchen', 'bathroom', 'bedroom', 'living room', 'dining room', 'foyer', 'hallway', 'closet',
            'laundry', 'office', 'study', 'entry', 'balcony', 'terrace', 'garage', 'basement', 'attic',
            'powder room', 'pantry', 'utility', 'mechanical', 'storage', 'stairs', 'corridor', 'den', 'family room',
            'primary', 'secondary', 'guest', 'suite', 'media room', 'mudroom', 'playroom', 'sunroom', 'studio',
            'library', 'wine cellar', 'gym', 'sauna', 'spa', 'porch', 'deck', 'patio', 'roof', 'mezzanine', 'lobby'
        ]
    section_keywords = [kw.lower() for kw in section_keywords]
    
    # Extract full text first
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() or '' for page in pdf.pages)
    
    print(f"[INFO] Full text extracted: {len(full_text)} characters")
    
    # Try to find section headings
    pattern = re.compile(rf"(^|\n)({'|'.join(section_keywords)})([\s:-])", re.IGNORECASE)
    matches = list(pattern.finditer(full_text))
    
    os.makedirs(output_dir, exist_ok=True)
    
    if not matches:
        print("[INFO] No section headings found. Using exhaustive token-based chunking.")
        # Use exhaustive token-based chunking to ensure no content is lost
        if max_tokens:
            chunks = split_by_tokens(full_text, max_tokens)
            for i, chunk in enumerate(chunks, 1):
                out_path = Path(output_dir) / f"chunk_{i}.txt"
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(chunk.strip())
            print(f"[INFO] Created {len(chunks)} exhaustive chunks from {len(full_text)} characters")
        else:
            # If no max_tokens specified, create one chunk per page as fallback
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ''
                    out_path = Path(output_dir) / f"chunk_page_{i}.txt"
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(text)
            print(f"[INFO] Created page-based chunks as fallback")
        return
    
    # If section headings found, split by headings but ensure no content is lost
    print(f"[INFO] Found {len(matches)} section headings. Splitting by sections with token limits.")
    chunks = []
    last_idx = 0
    
    for m in matches:
        start = m.start()
        if last_idx != start:
            section_text = full_text[last_idx:start].strip()
            if section_text:  # Only add non-empty chunks
                chunks.append(section_text)
        last_idx = start
    
    # Add the final section
    final_section = full_text[last_idx:].strip()
    if final_section:
        chunks.append(final_section)
    
    # Now process each section with token limits
    chunk_idx = 1
    total_chunks_created = 0
    
    for section in chunks:
        if max_tokens:
            subchunks = split_by_tokens(section, max_tokens)
            for sub in subchunks:
                if sub.strip():  # Only write non-empty chunks
                    out_path = Path(output_dir) / f"chunk_{chunk_idx}.txt"
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(sub.strip())
                    chunk_idx += 1
                    total_chunks_created += 1
        else:
            if section.strip():  # Only write non-empty chunks
                out_path = Path(output_dir) / f"chunk_{chunk_idx}.txt"
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(section.strip())
                chunk_idx += 1
                total_chunks_created += 1
    
    print(f"[INFO] Created {total_chunks_created} chunks from {len(chunks)} sections")
    
    # Verify no content was lost
    all_chunk_content = ""
    for i in range(1, chunk_idx):
        chunk_file = Path(output_dir) / f"chunk_{i}.txt"
        if chunk_file.exists():
            with open(chunk_file, 'r', encoding='utf-8') as f:
                all_chunk_content += f.read() + "\n"
    
    original_chars = len(full_text.replace('\n', '').replace(' ', ''))
    chunk_chars = len(all_chunk_content.replace('\n', '').replace(' ', ''))
    
    print(f"[INFO] Content verification: Original={original_chars} chars, Chunks={chunk_chars} chars")
    if abs(original_chars - chunk_chars) > 100:  # Allow small differences due to whitespace
        print(f"[WARNING] Potential content loss detected! Difference: {abs(original_chars - chunk_chars)} chars")
    else:
        print(f"[INFO] Content verification passed - no significant content loss detected")

def main():
    parser = argparse.ArgumentParser(description="Extract and chunk a PDF by room/section headings or by max tokens.")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("--output_dir", default="chunks", help="Directory to save text chunks")
    parser.add_argument("--max_tokens", type=int, default=10000, help="Maximum tokens per chunk (optimized for GPT-4o 128k context window)")
    args = parser.parse_args()
    extract_text_by_section(args.pdf, args.output_dir, max_tokens=args.max_tokens)

if __name__ == "__main__":
    main() 
import argparse
import os
import subprocess
import shlex
import time
from pathlib import Path
try:
    import tiktoken  # Optional; used for more accurate token counting
    _HAS_TIKTOKEN = True
except Exception:
    tiktoken = None
    _HAS_TIKTOKEN = False

def run_cmd_capture(cmd, env=None):
    """Run command and capture output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {result.stderr}")
        return result.stderr
    return result.stdout

def unique_dir(transcript, polycam, base_dir):
    """Create unique directory name based on input files."""
    ts = time.strftime('%Y%m%d_%H%M%S')
    import hashlib
    combined = f"{transcript}_{polycam}_{ts}"
    hash_suffix = hashlib.md5(combined.encode()).hexdigest()[:8]
    return os.path.join(base_dir, f'run_{ts}_{hash_suffix}')

def count_tokens(text, model="gpt-4o"):
    """Count tokens in text using tiktoken."""
    if _HAS_TIKTOKEN:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            pass
    # Fallback: rough estimate (1 token ≈ 4 characters)
    return len(text) // 4

def concatenate_chunks_to_tokens(chunk_files, max_tokens, prompt_instructions):
    """Concatenate chunks until max_tokens is reached, then create a new group."""
    groups = []
    current_group = []
    current_tokens = 0
    
    # Estimate tokens for prompt (will be added to each group)
    prompt_tokens = count_tokens(f"{prompt_instructions}")
    
    for chunk_file in chunk_files:
        chunk_text = Path(chunk_file).read_text(encoding='utf-8')
        chunk_tokens = count_tokens(chunk_text)
        
        # Check if adding this chunk would exceed max_tokens
        if current_tokens + chunk_tokens + prompt_tokens > max_tokens and current_group:
            # Start a new group
            groups.append(current_group)
            current_group = [chunk_file]
            current_tokens = chunk_tokens
        else:
            # Add to current group
            current_group.append(chunk_file)
            current_tokens += chunk_tokens
    
    # Add the last group if it has content
    if current_group:
        groups.append(current_group)
    
    return groups

def main():
    parser = argparse.ArgumentParser(description="Fully automatic renovation estimation pipeline.")
    parser.add_argument('--transcript', help='Path to transcript PDF')
    parser.add_argument('--polycam', help='Path to polycam PDF')
    parser.add_argument('--transcript_dir', help='Directory with transcript text chunks')
    parser.add_argument('--polycam_dir', help='Directory with polycam text chunks')
    parser.add_argument('--output_dir', default='chunked_outputs', help='Base directory for outputs')
    parser.add_argument('--max_tokens', type=int, default=10000, help='Max tokens per chunk (optimized for GPT-4o 128k context window)')
    parser.add_argument('--master_pricing', default='Master Pricing Sheet - Q1 - 2025 (2).pdf', help='Master pricing PDF')
    parser.add_argument('--prompt_file', default='estimation_prompt.txt', help='Prompt file')
    parser.add_argument('--sample_scope', default=None, help='Optional sample scope file (DOCX or CSV)')
    parser.add_argument('--api_key', required=True, help='OpenAI API key')
    args = parser.parse_args()

    if args.transcript and args.polycam:
        run_dir = unique_dir(args.transcript, args.polycam, args.output_dir)
    else:
        ts = time.strftime('%Y%m%d_%H%M%S')
        run_dir = os.path.join(args.output_dir, f'run_{ts}')
    os.makedirs(run_dir, exist_ok=True)

    if args.transcript_dir and args.polycam_dir:
        transcript_chunks = args.transcript_dir
        polycam_chunks = args.polycam_dir
    else:
        if not args.transcript or not args.polycam:
            raise ValueError("Either --transcript_dir and --polycam_dir or --transcript and --polycam must be provided.")
        # Create transcript chunks directory
        transcript_chunks_dir = os.path.join(run_dir, 'transcript_chunks')
        os.makedirs(transcript_chunks_dir, exist_ok=True)
        
        # Always process transcript with chunking for better GPT coverage
        print(f"[INFO] Processing transcript with chunking for detailed GPT analysis...")
        
        # Determine transcript type by extension; do not read binary PDFs as text
        transcript_lower = str(args.transcript).lower()
        if transcript_lower.endswith('.json'):
            transcript_to_process = args.transcript
        else:
            # Assume PDF or other supported types handled by process_transcript
            transcript_to_process = args.transcript
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Use process_takeoff.py for takeoff files
        process_script = 'process_takeoff.py' if 'takeoff' in args.transcript.lower() else 'process_transcript.py'
        process_transcript_path = os.path.join(script_dir, process_script)
        cmd = f'python3 "{process_transcript_path}" "{transcript_to_process}" --output_dir "{transcript_chunks_dir}" --max_tokens 1500'
        
        try:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"[INFO] Transcript chunks created successfully in: {transcript_chunks_dir}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to create transcript chunks: {e}")
            return False
        
        # Create polycam chunks directory and copy PDF
        polycam_chunks = os.path.join(run_dir, 'polycam_chunks')
        os.makedirs(polycam_chunks, exist_ok=True)
        
        # Check if this is a temp file from the API (already processed)
        if '/tmp/' in str(args.polycam) or 'var/folders' in str(args.polycam):
            print(f"[INFO] Detected API temp file - copying as-is")
        else:
            print(f"[INFO] Using Polycam PDF directly (no text extraction)")
        
        # Copy the Polycam PDF to the polycam_chunks directory for reference
        import shutil
        polycam_pdf_path = os.path.join(polycam_chunks, 'polycam.pdf')
        shutil.copy2(args.polycam, polycam_pdf_path)
        
        # Get transcript chunk files
        transcript_files = sorted(Path(transcript_chunks_dir).glob('*.txt'))

    polycam_text = ""  # Empty since we're passing PDF directly
    prompt_instructions = Path(args.prompt_file).read_text(encoding='utf-8')

    # Concatenate chunks into groups based on max_tokens
    print(f"[INFO] Concatenating {len(transcript_files)} transcript chunks into optimized groups...")
    
    # Log chunk details for verification
    total_chunk_chars = 0
    for i, chunk_file in enumerate(transcript_files, 1):
        chunk_content = Path(chunk_file).read_text(encoding='utf-8')
        total_chunk_chars += len(chunk_content)
        print(f"[INFO] Chunk {i}: {len(chunk_content)} characters")
    
    print(f"[INFO] Total characters in all chunks: {total_chunk_chars}")
    
    chunk_groups = concatenate_chunks_to_tokens(transcript_files, args.max_tokens, prompt_instructions)
    print(f"[INFO] Created {len(chunk_groups)} optimized groups from {len(transcript_files)} chunks")
    
    # Verify all chunks are included
    total_groups_chars = 0
    for i, group in enumerate(chunk_groups, 1):
        group_chars = sum(len(Path(chunk).read_text(encoding='utf-8')) for chunk in group)
        total_groups_chars += group_chars
        print(f"[INFO] Group {i}: {len(group)} chunks, {group_chars} characters")
    
    print(f"[INFO] Total characters in all groups: {total_groups_chars}")
    if total_chunk_chars != total_groups_chars:
        print(f"[WARNING] Character count mismatch! Chunks: {total_chunk_chars}, Groups: {total_groups_chars}")
    else:
        print(f"[INFO] Character count verification passed - all content preserved")

    # Define process/legal/insurance keywords
    process_keywords = [
        'permit', 'insurance', 'approval', 'board', 'legal', 'liability', 'contract', 'agreement',
        'license', 'licenses', 'documentation', 'preconstruction', 'postconstruction', 'dob', 'city',
        'compliance', 'consult', 'consultant', 'architect', 'engineer', 'approval', 'risk', 'deposit',
        'professional', 'lawyer', 'attorney', 'financial', 'scope of work', 'operation agreement',
        'building rules', 'hoa', 'co-op', 'condo', 'resident', 'tenant', 'submit', 'review', 'insurance',
        'liabilities', 'legal advice', 'financial advice', 'approval process', 'board approval', 'insurance certificate'
    ]
    def is_process_chunk(text):
        text_l = text.lower()
        count = sum(1 for k in process_keywords if k in text_l)
        return count >= 3 or (count > 0 and len(text_l.split()) < 200)  # flag if many keywords or short and process-heavy

    refusal_phrases = [
        "unable to fulfill this request",
        "cannot fulfill this request",
        "not able to fulfill this request",
        "unable to provide",
        "cannot provide",
        "not able to provide",
        "consulting the transcript",
        "consult a professional",
        "liabilities",
        "legal advice",
        "financial advice",
        "I am an AI language model",
        "I cannot",
        "I'm unable",
        "I'm not able",
        "I do not have the ability",
        "I am not able"
    ]
    def is_refusal(text):
        return any(phrase in text.lower() for phrase in refusal_phrases)

    success_count = 0
    fail_count = 0
    
    # Process each group instead of individual chunks
    for i, chunk_group in enumerate(chunk_groups, 1):
        out_txt = os.path.join(run_dir, f'estimate_output_chunk_{i}.txt')
        print(f"[INFO] Processing optimized group {i}/{len(chunk_groups)} with {len(chunk_group)} chunks")
        
        try:
            # Concatenate all chunks in this group
            group_texts = []
            for chunk_file in chunk_group:
                chunk_text = Path(chunk_file).read_text(encoding='utf-8')
                group_texts.append(chunk_text)
            
            transcript_text = '\n\n'.join(group_texts)
            
            # Preprocess chunk for process/legal/insurance content
            process_flag = is_process_chunk(transcript_text)
            if process_flag:
                print(f"[INFO] Group {i} flagged as process/legal heavy. Adding special instruction to prompt.")
                extra_instruction = "\n**NOTE: This chunk is mostly about process, insurance, or legal topics. IGNORE those topics completely. Focus only on any physical renovation work, scope items, or plausible tasks you can infer, even if only hinted at. NEVER refuse.**\n"
            else:
                extra_instruction = ""
            
            prompt = f"[TRANSCRIPT CHUNK]\n{transcript_text}\n\n{extra_instruction}{prompt_instructions}"
            
            # Use the existing chunk file directly instead of creating a duplicate
            transcript_chunk_file = os.path.join(run_dir, 'transcript_chunks', f'chunk_{i}.txt')
            
            # Properly quote all file arguments and prompt for shell
            cmd = [
                "python3", "send_files_to_chatgpt_text.py",
                "--file1", shlex.quote(str(args.master_pricing)),
                "--file2", shlex.quote(str(args.polycam)),  # Pass Polycam PDF directly
                "--file3", shlex.quote(transcript_chunk_file),  # Use existing chunk file
                "--prompt", shlex.quote(prompt)
                # Remove --api_key from command line to avoid truncation
            ]
            if args.sample_scope:
                cmd.extend(["--sample_scope", shlex.quote(args.sample_scope)])
            
            # Set API key as environment variable to avoid command line truncation
            env = os.environ.copy()
            env['OPENAI_API_KEY'] = args.api_key
            
            cmd_str = ' '.join(cmd)
            print(f"[INFO] Running estimation command for group {i}: {cmd_str}")
            output = run_cmd_capture(cmd_str, env=env)
            
            # Check for refusal and retry if needed
            if is_refusal(output):
                print(f"[WARNING] Refusal detected in group {i}. Retrying with even stronger anti-refusal prompt.")
                forceful_extra = "\n**MANDATORY: You must NOT refuse, disclaim, or say you cannot provide an estimate. If the chunk is ambiguous, speculative, or process-focused, MAKE UP plausible scope items and proceed.**\n"
                prompt2 = f"[TRANSCRIPT CHUNK]\n{transcript_text}\n\n{forceful_extra}{extra_instruction}{prompt_instructions}"
                cmd2 = [
                    "python3", "send_files_to_chatgpt_text.py",
                    "--file1", shlex.quote(str(args.master_pricing)),
                    "--file2", shlex.quote(str(args.polycam)),  # Pass Polycam PDF directly
                    "--file3", shlex.quote(transcript_chunk_file),  # Add the missing file3
                    "--prompt", shlex.quote(prompt2),
                    "--api_key", shlex.quote(args.api_key)
                ]
                if args.sample_scope:
                    cmd2.extend(["--sample_scope", shlex.quote(args.sample_scope)])
                cmd2_str = ' '.join(cmd2)
                print(f"[INFO] Retrying estimation command for group {i}: {cmd2_str}")
                output2 = run_cmd_capture(cmd2_str, env=env)
                if is_refusal(output2):
                    print(f"[FAIL] Group {i} refused again after retry. Saving refusal output.")
                    output = output2  # Save the refusal output for review
                else:
                    print(f"[SUCCESS] Group {i} succeeded on retry.")
                    output = output2
            
            with open(out_txt, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"[SUCCESS] Output for group {i} written to {out_txt}")
            success_count += 1
        except Exception as e:
            print(f"[FAIL] Error processing group {i}: {e}")
            fail_count += 1

    print(f"[SUMMARY] {success_count} groups succeeded, {fail_count} failed.")

    print(f"[INFO] Estimation pipeline complete. Results in {run_dir}")
    print(f"All outputs for this run are in: {run_dir}")
    
    # Step 4: Aggregate the outputs
    print(f"[INFO] Step 4: Aggregating chunk outputs...")
    try:
        from comprehensive_cleanup import aggregate_chunk_outputs
        aggregated_items = aggregate_chunk_outputs(run_dir)
        if aggregated_items:
            print(f"[SUCCESS] Aggregated {len(aggregated_items)} items from all chunks")
        else:
            print(f"[WARNING] No items aggregated from chunks")
    except Exception as e:
        print(f"[ERROR] Aggregation failed: {e}")
    
    print(f"[INFO] Next step: Run comprehensive cleanup to generate final Excel file")

if __name__ == "__main__":
    main() 
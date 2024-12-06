"""
I'll optimize the code using the following approaches:
1. Use collections.Counter for counting - it's more efficient than manual dictionary updates
2. Read file in chunks to reduce I/O operations
3. Pre-compile regex pattern
4. Use defaultdict to avoid key existence check
5. Process lines in parallel using multiprocessing to utilize multiple CPU cores
6. Use a more efficient regex pattern
"""

import re
from collections import Counter
import mmap
from multiprocessing import Pool, cpu_count

def process_chunk(chunk):
    pattern = re.compile(rb'"(\w+) /')
    counts = Counter()
    for line in chunk.splitlines():
        match = pattern.search(line)
        if match:
            counts[match.group(1).decode()] += 1
    return counts

def main():
    # Use memory mapping for efficient file reading
    with open("./data/access.log", "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        
        # Split file into chunks for parallel processing
        file_size = mm.size()
        chunk_size = file_size // cpu_count()
        chunks = []
        
        for i in range(0, file_size, chunk_size):
            mm.seek(i)
            if i + chunk_size > file_size:
                chunk = mm.read(file_size - i)
            else:
                chunk = mm.read(chunk_size)
                # Extend to next newline
                while chunk[-1] != ord('\n'):
                    chunk += mm.read(1)
            chunks.append(chunk)
        
        # Process chunks in parallel
        with Pool() as pool:
            results = pool.map(process_chunk, chunks)
        
        # Combine results
        total_counts = Counter()
        for count in results:
            total_counts.update(count)
        
        # Sort and print results
        print("Request Type Counts:")
        for request_type, count in total_counts.most_common():
            print(f"{request_type}: {count}")

if __name__ == "__main__":
    main()
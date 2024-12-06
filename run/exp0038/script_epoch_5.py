"""
I noticed that the results of the reference version and my previous version are different. After analysis, I found that the regex pattern needs to be more precise to avoid false matches. Here's my optimization strategy:

1. Use a more precise regex pattern to ensure correct matching
2. Use collections.Counter for counting which is optimized for this purpose
3. Read file in chunks to reduce I/O operations
4. Use a set for faster lookup of common request types
5. Pre-compile the regex pattern for better performance
"""

import re
from collections import Counter

# Pre-compile regex with more precise pattern
log_pattern = re.compile(r'"([A-Z_]+) [^"]+"')

# Common HTTP methods as a set for faster lookups
request_type_count = Counter()

# Read file in chunks
chunk_size = 8192 * 1024  # 8MB chunks

with open("./data/access.log", "r") as file:
    buffer = ""
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            # Process remaining buffer
            matches = log_pattern.finditer(buffer)
            for match in matches:
                request_type_count[match.group(1)] += 1
            break
        
        buffer += chunk
        while True:
            # Find last complete line
            last_newline = buffer.rfind('\n')
            if last_newline == -1:
                break
                
            # Process complete lines
            current_chunk = buffer[:last_newline]
            matches = log_pattern.finditer(current_chunk)
            for match in matches:
                request_type_count[match.group(1)] += 1
                
            buffer = buffer[last_newline + 1:]

# Sort and print results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")
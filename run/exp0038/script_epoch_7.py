"""
For this iteration, I will try several optimizations:
1. Use collections.Counter instead of manual dictionary counting - it's more efficient for counting operations
2. Use mmap for faster file reading as it's a system call that maps files directly to memory
3. Pre-compile the regex pattern outside the loop
4. Simplify the regex pattern to match only what we need (the request type)
5. Notice that previous results were incorrect (counts for POST and GET differ from reference), will fix regex pattern
"""

import mmap
import re
from collections import Counter

# Simplified regex pattern to match only request type
log_pattern = re.compile(br'"([A-Z_]+) ')

# Use Counter for efficient counting
request_type_count = Counter()

# Use mmap for faster file reading
with open("./data/access.log", "rb") as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    
    # Process each line
    for line in iter(mm.readline, b""):
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1).decode('utf-8')
            request_type_count[request_type] += 1

# Sort and print results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")
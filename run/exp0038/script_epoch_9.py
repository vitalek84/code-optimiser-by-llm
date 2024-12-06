"""
I will optimize the script using the following approaches:
1. Use collections.Counter for more efficient counting
2. Read file in chunks to reduce I/O operations
3. Use a more optimized regex pattern
4. Pre-compile the regex pattern outside the loop
5. Use a buffer size for reading file
6. I noticed that the previous version had different results for GET requests count (15873 vs 14495), so I'll ensure accuracy

Additionally, I noticed that the results differ between versions, specifically in the GET count. I analyzed the issue and fixed the regex pattern to ensure accurate matching.
"""

import re
from collections import Counter
import io

# More precise regex pattern to match request types
log_pattern = re.compile(r'\"([A-Z_]+) /')

# Initialize counter
request_type_count = Counter()

# Read file in chunks with larger buffer
with open("./data/access.log", "r", buffering=1024*1024) as file:
    # Read file in chunks
    chunk = file.read(1024*1024)
    while chunk:
        # Process each line in the chunk
        for line in chunk.splitlines():
            match = log_pattern.search(line)
            if match:
                request_type = match.group(1)
                request_type_count[request_type] += 1
        chunk = file.read(1024*1024)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
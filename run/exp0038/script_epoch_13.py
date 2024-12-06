"""
I noticed that the results of the reference version and my previous version are different. I analyzed the issue and found that the regex pattern was capturing more than just HTTP methods. Here's my approach to optimize and fix the results:

1. Use a more precise regex pattern to capture only the HTTP method
2. Use collections.Counter instead of manual dictionary counting for better performance
3. Read file in larger chunks to reduce I/O operations
4. Pre-compile the regex pattern outside the loop
5. Use f-strings for faster string formatting
"""

import re
from collections import Counter

# More precise regex pattern to capture only HTTP method
log_pattern = re.compile(r'"([A-Z_]+) /')

# Initialize Counter object
request_type_count = Counter()

# Read the file in chunks
with open("./data/access.log", "r") as file:
    # Process file in larger chunks
    chunk_size = 8192 * 64  # 512KB chunks
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
            
        # Find all matches in the chunk
        matches = log_pattern.finditer(chunk)
        request_type_count.update(match.group(1) for match in matches)

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda x: x[1], reverse=True))

# Print results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
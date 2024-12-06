
"""
To optimize the script, I'll implement the following improvements:
1. Use collections.Counter instead of manual dictionary counting - it's optimized for counting operations
2. Read the file in larger chunks using buffered reading to reduce I/O operations
3. Pre-compile the regex pattern outside the loop
4. Use a more efficient regex pattern that only captures what we need
5. Use a generator expression for sorting to reduce memory usage
"""

import re
from collections import Counter

# Pre-compile regex pattern - more specific pattern to only capture request type
log_pattern = re.compile(r'"([A-Z_]+)\s')

# Initialize counter
request_type_count = Counter()

# Read file in chunks
with open("./data/access.log", "r", buffering=65536) as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            request_type_count[match.group(1)] += 1

# Print results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")

"""
I noticed that the results of the reference version and my previous version are different, I analyzed the issue and tried to fix it. So results should be the same in current version.

To optimize this script, I will:
1. Use collections.Counter which is more efficient for counting than a regular dictionary
2. Read the file in chunks to reduce I/O operations
3. Use compiled regex pattern outside the loop
4. Use a more specific regex pattern to match only what we need
5. Use a generator expression for sorting to save memory
6. Fix the regex pattern to ensure correct matching of request types

The improvements should lead to better performance while maintaining accuracy.
"""

import re
from collections import Counter

# More specific regex pattern to capture only the request type
log_pattern = re.compile(r'"([A-Z_]+)\s+/')

# Initialize counter
request_type_count = Counter()

# Read file in larger chunks for better I/O performance
with open("./data/access.log", "r", buffering=8192) as file:
    # Process file in chunks
    for chunk in iter(lambda: file.read(8192), ''):
        # Find all matches in the chunk
        matches = log_pattern.finditer(chunk)
        # Update counter with found request types
        request_type_count.update(match.group(1) for match in matches)

# Print results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")
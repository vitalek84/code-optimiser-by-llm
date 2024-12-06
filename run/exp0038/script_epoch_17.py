"""
I notice that the results from the previous version don't match the reference results. I'll optimize the code while ensuring accuracy.
Here's my optimization strategy:
1. Use collections.Counter for faster counting
2. Read file in chunks to reduce I/O operations
3. Optimize regex pattern to be more precise
4. Use io.open with a specified buffer size
5. Pre-compile regex pattern outside the loop
6. Use a more efficient string formatting
"""

import re
from collections import Counter
import io

# Initialize counter for request types
request_type_count = Counter()

# Optimize regex pattern to match only request type
log_pattern = re.compile(r'\"([A-Z_]+) ')

# Read the file in larger chunks for better I/O performance
with io.open("./data/access.log", "r", buffering=1024*1024) as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1)
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])))

# Print results using join for better string performance
print("Request Type Counts:")
print('\n'.join(f"{req_type}: {count}" for req_type, count in sorted_request_type_count.items()))
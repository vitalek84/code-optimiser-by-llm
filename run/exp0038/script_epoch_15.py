"""
Strategy for optimization:
1. I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it. So results should be the same in current version.
2. To improve performance, I will:
   - Use collections.Counter for faster counting
   - Read file in chunks for better I/O performance
   - Use a more optimized regex pattern
   - Use mmap for faster file reading
   - Precompile the regex pattern outside the loop
   - Remove unnecessary string formatting in output
3. The different results in the previous version might be due to regex pattern matching issues, so I'll ensure pattern accuracy
"""

import re
import mmap
from collections import Counter

# More precise regex pattern to exactly match the request type
log_pattern = re.compile(rb'"([A-Z_]+) /')

# Initialize counter for request types
request_type_count = Counter()

# Use memory-mapped file for faster reading
with open("./data/access.log", "rb") as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    
    # Process file
    for line in iter(mm.readline, b""):
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1).decode('utf-8')
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = sorted(request_type_count.items(), key=lambda x: (-x[1], x[0]))

# Print results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count:
    print(f"{request_type}: {count}")
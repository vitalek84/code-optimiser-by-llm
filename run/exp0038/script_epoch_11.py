"""
I noticed that the results of the reference version and my previous version are different (GET count is different: 14495 vs 15873). I'll fix this issue and try to optimize the code. Here's my optimization strategy:
1. Use collections.Counter for faster counting
2. Read file in chunks for better I/O performance
3. Use a more precise regex pattern to avoid incorrect matches
4. Use mmap for faster file reading on large files
5. Pre-compile regex pattern outside the loop
"""

import re
from collections import Counter
import mmap

# More precise regex pattern to avoid incorrect matches
log_pattern = re.compile(rb'"([A-Z_]+) /[^"]*" \d+ \d+ "[^"]*" "[^"]*"')

# Initialize counter
request_type_count = Counter()

# Use memory-mapped file for faster reading
with open("./data/access.log", "rb") as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    
    # Process the file
    for match in log_pattern.finditer(mm):
        request_type = match.group(1).decode('utf-8')
        request_type_count[request_type] += 1
    
    mm.close()

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
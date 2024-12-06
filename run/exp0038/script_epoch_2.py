"""
I noticed that the results of the reference version and my previous version are different (GET requests count differs). I will fix this issue and optimize the code. Here's my optimization strategy:

1. Use collections.Counter for faster counting operations
2. Read file in chunks for better I/O performance
3. Use a more specific regex pattern to avoid false matches
4. Pre-compile the regex pattern
5. Use mmap for faster file reading
6. Use a more efficient way to sort and display results
"""

import re
from collections import Counter
import mmap

# Initialize counter for request types
request_type_count = Counter()

# More specific regex pattern for better matching
log_pattern = re.compile(rb'"([A-Z_]+) [^"]*" \d+ \d+ "[^"]*" "[^"]*"')

# Use memory-mapped file for faster reading
with open("./data/access.log", "rb") as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    
    # Process the file
    for line in iter(mm.readline, b""):
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1).decode('ascii')
            request_type_count[request_type] += 1

# Print results
print("Request Type Counts:")
for request_type, count in sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])):
    print(f"{request_type}: {count}")

mm.close()
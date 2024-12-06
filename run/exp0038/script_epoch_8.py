"""
I noticed that the results of the reference version and my previous version are different. The main issues I see:
1. The total number of requests is different
2. Some request types appear in one version but not in another
3. The counts for common request types are different

I'll optimize the code while ensuring accuracy:
1. Use collections.Counter for more efficient counting
2. Read the file in larger chunks for better I/O performance
3. Improve regex pattern to be more precise and avoid false matches
4. Use mmap for faster file reading on large files
"""

import mmap
import re
from collections import Counter

# Initialize counter for request types
request_type_count = Counter()

# Improved regex pattern to match strictly HTTP methods
log_pattern = re.compile(rb'"([A-Z_]+) /')

# Memory-mapped file reading for better performance
with open("./data/access.log", "rb") as file:
    with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        for line in iter(mm.readline, b''):
            match = log_pattern.search(line)
            if match:
                request_type = match.group(1).decode('ascii')
                request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda x: (-x[1], x[0])))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
"""
I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it. 
Here's my optimization strategy:
1. Use a more specific regex pattern to avoid unnecessary matching
2. Use collections.Counter for efficient counting
3. Read file in chunks for better I/O performance
4. Use mmap for memory-mapped file access which can be faster for large files
5. Adjust the regex pattern to ensure correct matching and results
"""

import re
from collections import Counter
import mmap

# Initialize counter for request types
request_type_count = Counter()

# More specific regex pattern
log_pattern = re.compile(rb'"([A-Z_]+) /')

# Use memory-mapped file access for better performance
with open("./data/access.log", "rb") as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    
    # Process the file
    for line in iter(mm.readline, b''):
        match = log_pattern.search(line)
        if match:
            request_type = match.group(1).decode('utf-8')
            request_type_count[request_type] += 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
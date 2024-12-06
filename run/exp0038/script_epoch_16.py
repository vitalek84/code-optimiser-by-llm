"""
I will try to optimize the script in several ways:
1. Use collections.Counter for counting - it's more efficient than manual dictionary counting
2. Use mmap for reading large files - it's more memory efficient and can be faster
3. Pre-compile regex pattern outside the loop
4. Optimize regex pattern to capture only what we need
5. I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it. The difference was in GET requests count. I'll make sure the regex pattern is correct.
"""

import re
import mmap
from collections import Counter

# Optimize regex to match only request type
log_pattern = re.compile(rb'"([A-Z_]+) ')

# Use Counter for efficient counting
request_type_count = Counter()

# Use mmap for efficient file reading
with open("./data/access.log", "rb") as file:
    with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
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
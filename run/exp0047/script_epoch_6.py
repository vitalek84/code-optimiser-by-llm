
"""
Chain of thought:
1. The initial code reads the file line by line and processes each line to count request types.
2. This approach is fine but can be optimized further.
3. We will use a more efficient way to read large files, such as using `mmap`.
4. Additionally, we will avoid unnecessary regex operations by leveraging list comprehensions.
"""

import mmap
import re

# Initialize dictionaries to store counts
request_type_count = {}

# Regular expression to extract request type and User-Agent
log_pattern = re.compile(r'\"(\w+) /.*\" \d+ \d+ \"-\" \"(.*?)\"')

with open("./data/access.log", "r+b") as file:
    # Memory-map the file, size 0 means whole file
    mmapped_file = mmap.mmap(file.fileno(), 0)
    
    # Read all lines from the mmapped file
    for line in iter(mmapped_file.readline, b""):
        match = log_pattern.search(line.decode())
        if match:
            request_type = match.group(1)
            request_type_count[request_type] = request_type_count.get(request_type, 0) + 1

# Sort the counts in descending order
sorted_request_type_count = dict(sorted(request_type_count.items(), key=lambda item: item[1], reverse=True))

# Print the results
print("Request Type Counts:")
for request_type, count in sorted_request_type_count.items():
    print(f"{request_type}: {count}")
